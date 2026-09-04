import logging
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import BookingForm, ComplaintForm, DestinationForm, PackageForm, TransportBookingForm
from .models import Booking, Complaint, Destination, GalleryImage, TourPackage, TransportBooking


logger = logging.getLogger(__name__)


def _send_booking_notification(booking, package_label):
    """Send a completed booking to the configured FormSubmit email endpoint."""
    form_data = {
        '_subject': f'New booking request: {package_label}',
        '_template': 'table',
        '_captcha': 'false',
        '_replyto': booking.guest_email,
        # FormSubmit uses this conventional field to enable Reply-To and mail
        # features.  A descriptive "Customer email" field alone is not enough.
        'email': booking.guest_email,
        '_next': settings.BOOKING_SITE_URL,
        'Customer name': booking.guest_name,
        'Customer email': booking.guest_email,
        'Phone number': booking.guest_phone or 'Not provided',
        'WhatsApp number': booking.whatsapp_number or 'Not provided',
        'Package': booking.package_name or 'Not selected',
        'Country': booking.country or 'Not provided',
        'Travelers': booking.travelers,
        'Estimated total': booking.total_price or 'Price available on request',
        'Start date': booking.start_date or 'Not provided',
        'Return date': booking.return_date or 'Not provided',
        'Preferred contact': booking.get_contact_method_display(),
        'Special requests': booking.special_requests or 'None',
    }
    request = Request(
        settings.BOOKING_NOTIFICATION_URL,
        data=urlencode(form_data).encode('utf-8'),
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': settings.BOOKING_SITE_URL,
            'User-Agent': 'Zenji Adventures booking notifications',
        },
        method='POST',
    )
    try:
        with urlopen(request, timeout=10) as response:
            if not 200 <= response.status < 400:
                raise RuntimeError(f'FormSubmit returned HTTP {response.status}')
        return True
    except Exception:
        # A FormSubmit issue must not prevent a valid booking from being saved,
        # but it must be visible in the deployment logs for troubleshooting.
        logger.exception('Unable to send booking notification through FormSubmit.')
        return False


def _booking_form(request, initial=None, redirect_url=None):
    form = BookingForm(request.POST or None, initial=initial)

    if request.method == 'POST' and form.is_valid():
        booking = form.save()
        package_label = booking.package_name or 'your selected package'
        notification_sent = _send_booking_notification(booking, package_label)
        messages.success(
            request,
            f'Thanks {booking.guest_name}. Your booking request has been sent to our team.',
        )
        # The public site is a Vercel rewrite to Render.  A query parameter
        # keeps the confirmation visible even when the session cookie cannot
        # make the cross-domain round trip.
        notice = 'success' if notification_sent else 'saved'
        return form, redirect(f"{redirect_url or reverse('home')}?booking={notice}#booking")

    return form, None


def _send_complaint_notification(complaint):
    """Email a contact or complaint through the configured FormSubmit inbox."""
    form_data = {
        '_subject': f'New contact message from {complaint.name}',
        '_template': 'table',
        '_captcha': 'false',
        '_replyto': complaint.email,
        'email': complaint.email,
        '_next': f'{settings.BOOKING_SITE_URL.rstrip("/")}{reverse("contact")}',
        'Customer name': complaint.name,
        'Customer email': complaint.email,
        'Phone / WhatsApp': complaint.phone or 'Not provided',
        'Message or complaint': complaint.message,
    }
    request = Request(
        settings.CONTACT_NOTIFICATION_URL,
        data=urlencode(form_data).encode('utf-8'),
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': settings.BOOKING_SITE_URL,
            'User-Agent': 'Zenji Adventures contact notifications',
        },
        method='POST',
    )
    try:
        with urlopen(request, timeout=10) as response:
            if not 200 <= response.status < 400:
                raise RuntimeError(f'FormSubmit returned HTTP {response.status}')
        return True
    except Exception:
        logger.exception('Unable to send contact notification through FormSubmit.')
        return False


def _send_transport_notification(booking):
    """Send a transport request to the same configured booking mailbox."""
    form_data = {
        '_subject': 'New transport booking request',
        '_template': 'table',
        '_captcha': 'false',
        '_replyto': booking.guest_email,
        'email': booking.guest_email,
        '_next': f'{settings.BOOKING_SITE_URL.rstrip("/")}{reverse("transport")}',
        'Customer name': booking.guest_name,
        'Customer email': booking.guest_email,
        'Phone number': booking.guest_phone,
        'Pickup location': booking.pickup_location,
        'Drop-off location': booking.dropoff_location,
        'Pickup date': booking.pickup_date,
        'Pickup time': booking.pickup_time,
        'Passengers': booking.passengers,
        'Vehicle preference': booking.get_vehicle_type_display(),
        'Special requests': booking.special_requests or 'None',
    }
    request = Request(
        settings.BOOKING_NOTIFICATION_URL,
        data=urlencode(form_data).encode('utf-8'),
        headers={'Content-Type': 'application/x-www-form-urlencoded', 'Referer': settings.BOOKING_SITE_URL, 'User-Agent': 'Zenji Adventures transport bookings'},
        method='POST',
    )
    try:
        with urlopen(request, timeout=10) as response:
            if not 200 <= response.status < 400:
                raise RuntimeError(f'FormSubmit returned HTTP {response.status}')
        return True
    except Exception:
        logger.exception('Unable to send transport notification through FormSubmit.')
        return False


def home(request):
    # Show every published package on the homepage.  Previously only the
    # first three (with popular packages first) were rendered, which hid newly
    # created packages from visitors.
    packages = TourPackage.objects.select_related('destination').order_by(
        '-is_popular', '-created_at'
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
    }
    return render(request, 'tour_app/index.html', context)


def contact(request):
    form = ComplaintForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        complaint = form.save()
        notification_sent = _send_complaint_notification(complaint)
        notice = 'success' if notification_sent else 'saved'
        return redirect(f"{reverse('contact')}?contact={notice}")

    return render(request, 'tour_app/contact.html', {
        'contact_form': form,
        'contact_notice': request.GET.get('contact'),
    })


def transport(request):
    form = TransportBookingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        booking = form.save()
        notification_sent = _send_transport_notification(booking)
        notice = 'success' if notification_sent else 'saved'
        return redirect(f"{reverse('transport')}?transport={notice}#transport-booking")

    return render(request, 'tour_app/transport.html', {
        'transport_form': form,
        'transport_notice': request.GET.get('transport'),
    })


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
        'booking_notice': request.GET.get('booking'),
    }
    return render(request, 'tour_app/packages.html', context)


def gallery(request):
    return render(request, 'tour_app/gallery.html', {
        'gallery_images': GalleryImage.objects.all(),
    })


def package_detail_by_id(request, pk):
    """Redirect old ID-based package URLs to their canonical slug URL."""
    package = get_object_or_404(TourPackage, pk=pk)
    return redirect('package_detail', slug=package.slug, permanent=True)


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
        'booking_notice': request.GET.get('booking'),
    }
    return render(request, 'tour_app/package_detail.html', context)


@staff_member_required
def dashboard(request):
    packages = TourPackage.objects.select_related('destination').annotate(
        booking_count=Count('bookings')
    ).order_by('-created_at')
    bookings = Booking.objects.select_related('package').order_by('-created_at')
    transport_bookings = TransportBooking.objects.all()

    context = {
        'packages': packages,
        'destinations': Destination.objects.annotate(package_count=Count('packages')).order_by('name'),
        'bookings': bookings,
        'transport_bookings': transport_bookings,
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


@staff_member_required
def destination_create(request):
    return _destination_form(request)


@staff_member_required
def destination_edit(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    return _destination_form(request, destination=destination)


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


def _destination_form(request, destination=None):
    form = DestinationForm(request.POST or None, instance=destination)

    if request.method == 'POST' and form.is_valid():
        saved_destination = form.save()
        action = 'updated' if destination else 'created'
        messages.success(request, f'Destination "{saved_destination.name}" has been {action}.')
        return redirect('dashboard')

    return render(request, 'tour_app/destination_form.html', {
        'form': form,
        'destination': destination,
        'is_edit': destination is not None,
    })


@staff_member_required
def package_delete(request, pk):
    package = get_object_or_404(TourPackage, pk=pk)

    if request.method == 'POST':
        title = package.title
        package.delete()
        messages.success(request, f'Package "{title}" has been deleted.')
        return redirect('dashboard')

    return render(request, 'tour_app/package_confirm_delete.html', {'package': package})
