from django.db import models


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

    def __str__(self):
        return self.title


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )

    guest_name = models.CharField(max_length=120)
    guest_email = models.EmailField()
    package = models.ForeignKey(TourPackage, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    travelers = models.PositiveIntegerField(default=1)
    start_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guest_name} - {self.package or 'Tour'}"
