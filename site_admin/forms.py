from django import forms

from tour_app.forms import DestinationForm, GalleryImageForm, PackageForm
from tour_app.models import Booking, Complaint, TransportBooking


class BookingAdminForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ('created_at',)
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 4}),
        }


class TransportBookingAdminForm(forms.ModelForm):
    class Meta:
        model = TransportBooking
        exclude = ('created_at',)
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date'}),
            'pickup_time': forms.TimeInput(attrs={'type': 'time'}),
            'special_requests': forms.Textarea(attrs={'rows': 4}),
        }


class ComplaintAdminForm(forms.ModelForm):
    class Meta:
        model = Complaint
        exclude = ('created_at',)
        widgets = {'message': forms.Textarea(attrs={'rows': 7})}
