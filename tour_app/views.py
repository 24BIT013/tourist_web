import logging
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import BookingForm, PackageForm
from .models import Booking, TourPackage


logger = logging.getLogger(__name__)


def _booking_summary(booking):
    return '\n'.join([
        'New booking request',
        f'Name: {booking.guest_name}',
        f'Email: {booking.guest_email}',
        f'Phone: {booking.guest_phone or "Not provided"}',
        f'WhatsApp: {booking.whatsapp_number or "Not provided"}',
        f'Package: {booking.package_name or "Not selected"}',
        f'Country: {booking.country or "Not provided"}',
        f'Travelers: {booking.travelers}',
        f'Start date: {booking.start_date or "Not provided"}',
        f'Return date: {booking.return_date or "Not provided"}',
        f'Preferred contact: {booking.get_contact_method_display()}',
        f'Special requests: {booking.special_requests or "None"}',
    ])


def _whatsapp_booking_url(summary):
    phone_number = ''.join(ch for ch in str(settings.WHATSAPP_PHONE_NUMBER) if ch.isdigit())
    return f'https://wa.me/{phone_number}?{urlencode({"text": summary})}'


def _send_booking_notification(booking, package_label):
    """Send a completed booking to the configured FormSubmit email endpoint."""
    form_data = {
        '_subject': f'New booking request: {package_label}',
        '_template': 'table',
        '_captcha': 'false',
        '_replyto': booking.guest_email,
        'Customer name': booking.guest_name,
        'Customer email': booking.guest_email,
        'Phone number': booking.guest_phone or 'Not provided',
        'WhatsApp number': booking.whatsapp_number or 'Not provided',
        'Package': booking.package_name or 'Not selected',
        'Country': booking.country or 'Not provided',
        'Travelers': booking.travelers,
        'Start date': booking.start_date or 'Not provided',
        'Return date': booking.return_date or 'Not provided',
        'Preferred contact': booking.get_contact_method_display(),
        'Special requests': booking.special_requests or 'None',
    }
    request = Request(
        settings.BOOKING_NOTIFICATION_URL,
        data=urlencode(form_data).encode('utf-8'),
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        method='POST',
    )
    try:
        with urlopen(request, timeout=10):
            pass
    except Exception:
        # A FormSubmit issue must not prevent a valid booking from being saved.
        logger.exception('Unable to send booking notification through FormSubmit.')


def _booking_form(request, initial=None, redirect_url=None):
    form = BookingForm(request.POST or None, initial=initial)

    if request.method == 'POST' and form.is_valid():
        booking = form.save()
        package_label = booking.package_name or 'your selected package'
        summary = _booking_summary(booking)
        _send_booking_notification(booking, package_label)
        messages.success(
            request,
            f'Thanks {booking.guest_name}. Opening WhatsApp to send your booking request.',
        )
        return form, redirect(_whatsapp_booking_url(summary))

    return form, None


def home(request):
    booking_form, booking_response = _booking_form(request, redirect_url=reverse('home'))
    if booking_response:
        return booking_response

    packages = list(
        TourPackage.objects.select_related('destination').order_by('-is_popular', '-created_at')[:3]
    )
    stats = [
        {'label': 'Happy Travelers', 'value': '24K+'},
        {'label': 'Destinations', 'value': '48+'},
        {'label': 'Expert Guides', 'value': '120'},
        {'label': 'Travel Awards', 'value': '16'},
    ]

    context = {
        'packages': packages,
        'stats': stats,
        'booking_form': booking_form,
        'booking_packages': TourPackage.objects.order_by('title'),
        'booking_action': reverse('home'),
    }
    return render(request, 'tour_app/index.html', context)


def packages(request):
    booking_form, booking_response = _booking_form(request, redirect_url=reverse('packages'))
    if booking_response:
        return booking_response

    package_list = list(TourPackage.objects.select_related('destination').order_by('-is_popular', '-created_at'))
    context = {
        'packages': package_list,
        'booking_form': booking_form,
        'booking_packages': TourPackage.objects.order_by('title'),
        'booking_action': reverse('packages'),
    }
    return render(request, 'tour_app/packages.html', context)


def package_detail(request, slug):
    package = get_object_or_404(TourPackage.objects.select_related('destination'), slug=slug)
    booking_form, booking_response = _booking_form(
        request,
        initial={'package': package.pk},
        redirect_url=reverse('package_detail', kwargs={'slug': slug}),
    )
    if booking_response:
        return booking_response

    context = {
        'package': package,
        'booking_form': booking_form,
        'booking_packages': TourPackage.objects.order_by('title'),
        'booking_action': reverse('package_detail', kwargs={'slug': slug}),
    }
    return render(request, 'tour_app/package_detail.html', context)


@staff_member_required
def dashboard(request):
    packages = TourPackage.objects.select_related('destination').annotate(
        booking_count=Count('bookings')
    ).order_by('-created_at')
    bookings = Booking.objects.select_related('package').order_by('-created_at')

    context = {
        'packages': packages,
        'bookings': bookings,
        'stats': {
            'packages': packages.count(),
            'bookings': bookings.count(),
            'pending': bookings.filter(status=Booking.Status.PENDING).count(),
            'confirmed': bookings.filter(status=Booking.Status.CONFIRMED).count(),
        },
    }
    return render(request, 'tour_app/dashboard.html', context)


@staff_member_required
def package_create(request):
    return _package_form(request)


@staff_member_required
def package_edit(request, pk):
    package = get_object_or_404(TourPackage, pk=pk)
    return _package_form(request, package=package)


def _package_form(request, package=None):
    form = PackageForm(request.POST or None, instance=package)

    if request.method == 'POST' and form.is_valid():
        saved_package = form.save()
        action = 'updated' if package else 'created'
        messages.success(request, f'Package "{saved_package.title}" has been {action}.')
        return redirect('dashboard')

    context = {
        'form': form,
        'package': package,
        'is_edit': package is not None,
    }
    return render(request, 'tour_app/package_form.html', context)


@staff_member_required
def package_delete(request, pk):
    package = get_object_or_404(TourPackage, pk=pk)

    if request.method == 'POST':
        title = package.title
        package.delete()
        messages.success(request, f'Package "{title}" has been deleted.')
        return redirect('dashboard')

    return render(request, 'tour_app/package_confirm_delete.html', {'package': package})
