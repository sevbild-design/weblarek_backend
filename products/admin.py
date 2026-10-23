from django.contrib import admin

from products.models import Category, Products


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
        'image',
        'category',
        'description',
        'id',
    )
    fieldsets = (
        (None, {
            'fields': [
                'title',
                ('price', 'category'),
                'image',
                'description',
            ]
        }),
    )
