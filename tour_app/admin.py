from django.contrib import admin

from .models import Booking, Destination, TourPackage


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'duration', 'price', 'is_popular')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('country', 'is_popular')
    search_fields = ('title', 'country', 'description')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'guest_email', 'package', 'travelers', 'start_date', 'status')
    list_filter = ('status', 'package')
    search_fields = ('guest_name', 'guest_email')
