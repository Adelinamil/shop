from django.contrib import admin

from .models import ProductCategory, Product

admin.site.site_header = 'Мир цветов'


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    sortable_by = ['id', 'name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'name', 'price', 'amount', 'created_at']
    sortable_by = ['id', 'category', 'name', 'price', 'amount', 'created_at']
    list_filter = ['category', 'created_at', 'updated_at']
    search_fields = ['name', 'category__name']
    search_help_text = 'Поиск по названию и категории'
    prepopulated_fields = {'slug': ('name',)}
