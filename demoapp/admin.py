from django.contrib import admin
from .models import Blog, Stock, Item, Bill

# Customize the Stock admin interface
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'initial_stock', 'current_stock', 'total_sold')
    search_fields = ('category_name',)
    list_filter = ('category_name',)

# Customize the Item admin interface
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'stock')  # Display item name and associated stock category
    search_fields = ('item_name', 'stock__category_name')  # Allow searching by item name and category
    list_filter = ('stock',)  # Add a filter for stock categories

# Customize the Bill admin interface
@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_phone', 'purchase_date', 'Sub_total', 'GST', 'Total')
    search_fields = ('customer_name', 'customer_phone')
    list_filter = ('purchase_date',)
    readonly_fields = ('purchase_date', 'Sub_total', 'GST', 'Total', 'items')  # Add purchase_date to readonly_fields
    fieldsets = (
        ('Customer Details', {
            'fields': ('customer_name', 'customer_phone')
        }),
        ('Bill Summary', {
            'fields': ('purchase_date', 'Sub_total', 'GST', 'Total', 'items')
        }),
    )

# Register the Blog model
admin.site.register(Blog)