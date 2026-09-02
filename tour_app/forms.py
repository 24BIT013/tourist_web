from django import forms
from django.utils.text import slugify

from .models import Booking, Complaint, Destination, TourPackage, calculate_package_total


def _unique_slug(model, value, instance=None):
    base_slug = slugify(value) or 'item'
    slug = base_slug
    counter = 2
    queryset = model.objects.all()
    if instance and instance.pk:
        queryset = queryset.exclude(pk=instance.pk)
    while queryset.filter(slug=slug).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1
    return slug


class PackageForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = [
            'title',
            'slug',
            'destination',
            'country',
            'duration',
            'price',
            'summary',
            'description',
            'image',
            'is_popular',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Safari in Kenya'}),
            'slug': forms.TextInput(attrs={'placeholder': 'safari-in-kenya'}),
            'destination': forms.Select(attrs={'class': 'form-select'}),
            'country': forms.TextInput(attrs={'placeholder': 'Kenya'}),
            'duration': forms.TextInput(attrs={'placeholder': '7 Days / 6 Nights'}),
            'price': forms.TextInput(attrs={'placeholder': '$1,250'}),
            'summary': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Short package summary'}),
            'description': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Full package description'}),
            'image': forms.URLInput(attrs={'placeholder': 'https://example.com/image.jpg'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['destination'].required = False
        self.fields['destination'].queryset = Destination.objects.order_by('name')
        self.fields['destination'].empty_label = 'Select a destination'

    def clean(self):
        cleaned_data = super().clean()
        destination = cleaned_data.get('destination')
        country = cleaned_data.get('country')
        if destination and not country:
            cleaned_data['country'] = destination.country
        return cleaned_data

    def save(self, commit=True):
        package = super().save(commit=False)
        if not package.slug:
            package.slug = _unique_slug(TourPackage, package.title, instance=package)
        if package.destination and not package.country:
            package.country = package.destination.country
        if commit:
            package.save()
        return package


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'country', 'description', 'image_url']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Zanzibar'}),
            'country': forms.TextInput(attrs={'placeholder': 'Tanzania'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'What makes this destination special?'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'https://example.com/destination.jpg'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'guest_name',
            'guest_email',
            'guest_phone',
            'whatsapp_number',
            'package',
            'travelers',
            'start_date',
            'return_date',
            'contact_method',
            'special_requests',
        ]
        widgets = {
            'guest_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'guest_email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            'guest_phone': forms.TextInput(attrs={'placeholder': '+254 700 000 000'}),
            'whatsapp_number': forms.TextInput(attrs={'placeholder': '+254 700 000 000'}),
            'package': forms.Select(attrs={'class': 'form-select'}),
            'travelers': forms.NumberInput(attrs={'min': 1, 'max': 50}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
            'contact_method': forms.Select(attrs={'class': 'form-select'}),
            'special_requests': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about your ideal trip'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['package'].queryset = TourPackage.objects.order_by('title')
        self.fields['package'].empty_label = 'Select a package'

    def save(self, commit=True):
        booking = super().save(commit=False)
        if booking.package:
            booking.total_price = calculate_package_total(
                booking.package.price, booking.travelers
            )
        if commit:
            booking.save()
        return booking


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '+255 700 000 000 (optional)'}),
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us how we can help or describe your complaint.'}),
        }
