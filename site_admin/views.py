from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from tour_app.models import Booking, Complaint, Destination, GalleryImage, TourPackage, TransportBooking

from .forms import (
    BookingAdminForm, ComplaintAdminForm, DestinationForm, GalleryImageForm,
    PackageForm, TransportBookingAdminForm,
)


SECTIONS = {
    'tours': {'label': 'Tours', 'singular': 'tour', 'model': TourPackage, 'form': PackageForm},
    'gallery': {'label': 'Gallery photos', 'singular': 'gallery photo', 'model': GalleryImage, 'form': GalleryImageForm},
    'destinations': {'label': 'Destinations', 'singular': 'destination', 'model': Destination, 'form': DestinationForm},
    'bookings': {'label': 'Tour bookings', 'singular': 'tour booking', 'model': Booking, 'form': BookingAdminForm},
    'transport': {'label': 'Transport bookings', 'singular': 'transport booking', 'model': TransportBooking, 'form': TransportBookingAdminForm},
    'messages': {'label': 'Contact messages', 'singular': 'contact message', 'model': Complaint, 'form': ComplaintAdminForm},
}


class ManagementLoginView(LoginView):
    """Sign staff into the website's own management area, not /admin/."""

    template_name = 'site_admin/login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = False

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_staff:
            form.add_error(None, 'This account does not have website management access.')
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy('site_admin:dashboard')


def management_logout(request):
    logout(request)
    return redirect('site_admin:login')


def _section_or_404(section):
    try:
        return SECTIONS[section]
    except KeyError as error:
        raise Http404('Unknown management section.') from error


@staff_member_required(login_url='site_admin:login')
def dashboard(request):
    sections = []
    for slug, config in SECTIONS.items():
        queryset = config['model'].objects.all()
        sections.append({
            'slug': slug,
            'label': config['label'],
            'count': queryset.count(),
            'records': queryset[:6],
        })
    return render(request, 'site_admin/dashboard.html', {
        'sections': sections,
        'stats': {
            'tours': TourPackage.objects.count(),
            'gallery': GalleryImage.objects.count(),
            'bookings': Booking.objects.count(),
            'pending': Booking.objects.filter(status=Booking.Status.PENDING).count(),
        },
    })


@staff_member_required(login_url='site_admin:login')
def record_create(request, section):
    config = _section_or_404(section)
    form = config['form'](request.POST or None)
    if request.method == 'POST' and form.is_valid():
        record = form.save()
        messages.success(request, f'{config["singular"].capitalize()} "{record}" has been added.')
        return redirect('site_admin:dashboard')
    return render(request, 'site_admin/record_form.html', {
        'form': form, 'section': section, 'config': config, 'record': None,
    })


@staff_member_required(login_url='site_admin:login')
def record_edit(request, section, pk):
    config = _section_or_404(section)
    record = get_object_or_404(config['model'], pk=pk)
    form = config['form'](request.POST or None, instance=record)
    if request.method == 'POST' and form.is_valid():
        record = form.save()
        messages.success(request, f'{config["singular"].capitalize()} "{record}" has been updated.')
        return redirect('site_admin:dashboard')
    return render(request, 'site_admin/record_form.html', {
        'form': form, 'section': section, 'config': config, 'record': record,
    })


@staff_member_required(login_url='site_admin:login')
def record_delete(request, section, pk):
    config = _section_or_404(section)
    record = get_object_or_404(config['model'], pk=pk)
    if request.method == 'POST':
        label = str(record)
        record.delete()
        messages.success(request, f'{config["singular"].capitalize()} "{label}" has been deleted.')
        return redirect('site_admin:dashboard')
    return render(request, 'site_admin/record_confirm_delete.html', {
        'section': section, 'config': config, 'record': record,
    })
