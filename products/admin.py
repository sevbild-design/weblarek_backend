from django.contrib import admin

from products.models import Category, Products, Order, OrderCounter


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

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'total',
        'id',
        'created_at'
    )
# @admin.register(OrderCounter)
# class OrderCounterAdmin(admin.ModelAdmin):
#     list_display = (
#         'last_number',
#     )