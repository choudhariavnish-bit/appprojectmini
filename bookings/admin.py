from django.contrib import admin
from .models import MasterBooking

@admin.register(MasterBooking)
class MasterBookingAdmin(admin.ModelAdmin):
    # This makes the admin panel show columns instead of just "MasterBooking object"
    list_display = ('customer_name', 'category', 'total_bill', 'is_delivery')