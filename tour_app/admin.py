from django.contrib import admin

from .models import Booking, Destination, TourPackage


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country', 'description')


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'duration', 'price', 'is_popular', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('country', 'is_popular', 'destination')
    search_fields = ('title', 'country', 'duration', 'description', 'summary', 'slug')
    autocomplete_fields = ('destination',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'guest_name',
        'guest_email',
        'guest_phone',
        'whatsapp_number',
        'package_name',
        'package',
        'travelers',
        'status',
        'created_at',
    )
    list_filter = ('status', 'contact_method', 'package', 'country')
    search_fields = ('guest_name', 'guest_email', 'guest_phone', 'whatsapp_number', 'package_name', 'country')
    readonly_fields = ('created_at',)
