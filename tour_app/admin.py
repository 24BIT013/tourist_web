from django.contrib import admin

from .models import Booking, Complaint, Destination, GalleryImage, TourPackage

admin.site.site_header = 'Zanji Adventures Administration'
admin.site.site_title = 'Zanji Adventures Admin'
admin.site.index_title = 'Manage Zanzibar tours, gallery images, and customer bookings'


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'country', 'description')


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'duration', 'price', 'is_popular', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('country', 'is_popular', 'destination')
    search_fields = ('title', 'country', 'duration', 'description', 'summary', 'slug')
    autocomplete_fields = ('destination',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Tour details', {
            'fields': ('title', 'slug', 'destination', 'country', 'duration', 'price'),
        }),
        ('Description and image', {
            'fields': ('summary', 'description', 'image', 'is_popular'),
        }),
        ('Record information', {'fields': ('created_at',)}),
    )


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_url', 'created_at')
    search_fields = ('title', 'caption')
    readonly_fields = ('created_at',)


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
        'total_price',
        'status',
        'created_at',
    )
    list_filter = ('status', 'contact_method', 'package', 'country')
    search_fields = ('guest_name', 'guest_email', 'guest_phone', 'whatsapp_number', 'package_name', 'country')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    list_select_related = ('package',)
    actions = ('mark_confirmed', 'mark_cancelled')
    fieldsets = (
        ('Guest', {'fields': ('guest_name', 'guest_email', 'guest_phone', 'whatsapp_number', 'country')}),
        ('Tour and dates', {'fields': ('package', 'package_name', 'travelers', 'total_price', 'start_date', 'return_date')}),
        ('Booking management', {'fields': ('contact_method', 'special_requests', 'status', 'created_at')}),
    )

    @admin.action(description='Mark selected bookings as confirmed')
    def mark_confirmed(self, request, queryset):
        queryset.update(status=Booking.Status.CONFIRMED)

    @admin.action(description='Mark selected bookings as cancelled')
    def mark_cancelled(self, request, queryset):
        queryset.update(status=Booking.Status.CANCELLED)


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
