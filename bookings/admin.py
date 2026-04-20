from django.contrib import admin
from .models import MasterBooking

@admin.register(MasterBooking)
class MasterBookingAdmin(admin.ModelAdmin):
    # Columns to show in the list
    list_display = ('id', 'customer_name', 'category', 'total_bill', 'is_delivery', 'created_at')
    
    # Clickable links
    list_display_links = ('id', 'customer_name')
    
    # Sidebar filters (Perfect for your multi-module app)
    list_filter = ('category', 'is_delivery', 'created_at')
    
    # Search box for names or specific details
    search_fields = ('customer_name', 'details')
    
    # Grouping the detail view
    fieldsets = (
        ("Customer Info", {
            'fields': ('customer_name', 'category')
        }),
        ("Transaction Details", {
            'fields': ('details', 'total_bill', 'is_delivery')
        }),
    )