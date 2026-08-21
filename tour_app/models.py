from django.db import models
from django.utils.text import slugify


class Destination(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class TourPackage(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='packages', null=True, blank=True)
    country = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    is_popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'

    class ContactMethod(models.TextChoices):
        WHATSAPP = 'whatsapp', 'WhatsApp'
        EMAIL = 'email', 'Email'
        PHONE = 'phone', 'Phone Call'

    guest_name = models.CharField(max_length=120)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=30, blank=True, default='')
    whatsapp_number = models.CharField(max_length=30, blank=True, default='')
    country = models.CharField(max_length=100, blank=True, default='')
    package = models.ForeignKey(TourPackage, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    package_name = models.CharField(max_length=150, blank=True, default='')
    travelers = models.PositiveIntegerField(default=1)
    start_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    contact_method = models.CharField(max_length=20, choices=ContactMethod.choices, default=ContactMethod.WHATSAPP)
    special_requests = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.package:
            self.package_name = self.package_name or self.package.title
            self.country = self.country or self.package.country
        super().save(*args, **kwargs)

    def __str__(self):
        package_label = self.package_name or (self.package.title if self.package else 'Tour')
        return f"{self.guest_name} - {package_label}"
