from django.db import migrations
from django.db.models import Max


def initialize_order_counter(apps, schema_editor):
    Order = apps.get_model('products', 'Order')
    OrderCounter = apps.get_model('products', 'OrderCounter')

    db_alias = schema_editor.connection.alias

    max_number = (
        Order.objects.using(db_alias)
        .aggregate(Max('number'))['number__max'] or 0
    )

    counter, created = (
        OrderCounter.objects.using(db_alias)
        .get_or_create(
            pk=1,
            defaults={'last_number': max_number},
        )
    )

    if not created and counter.last_number < max_number:
        counter.last_number = max_number
        counter.save(
            using=db_alias,
            update_fields=['last_number'],
        )


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_order_created_at'),
    ]

    operations = [
        migrations.RunPython(
            initialize_order_counter,
            migrations.RunPython.noop,
        ),
    ]
