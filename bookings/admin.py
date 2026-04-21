from django.contrib import admin
from .models import MasterBooking

@admin.register(MasterBooking)
class MasterBookingAdmin(admin.ModelAdmin):
    # This tells Django exactly which columns to show in the list
    list_display = ('customer_name', 'category', 'total_bill', 'details')
    
    # This allows you to click the category to filter (e.g., see only CAFE)
    list_filter = ('category',)