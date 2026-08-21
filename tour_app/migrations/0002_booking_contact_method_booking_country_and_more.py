# Generated manually to add richer booking records and seed the initial package catalog.

from django.db import migrations, models
import django.db.models.deletion


def seed_initial_packages(apps, schema_editor):
    Destination = apps.get_model('tour_app', 'Destination')
    TourPackage = apps.get_model('tour_app', 'TourPackage')

    packages = [
        {
            'title': 'Bali Island Escape',
            'slug': 'bali-island-escape',
            'country': 'Indonesia',
            'duration': '5 Days / 4 Nights',
            'price': '$649',
            'summary': 'Chase islands, temples, beaches, and a slower rhythm of island life.',
            'description': 'A relaxing island journey with scenic stays, cultural stops, and time to unwind by the ocean.',
            'image': 'https://images.unsplash.com/photo-1537996194471-e657df8fabcc?auto=format&fit=crop&q=80',
            'is_popular': True,
            'destination': {
                'name': 'Bali',
                'country': 'Indonesia',
                'description': 'A tropical island known for beaches, rice terraces, and wellness retreats.',
                'image_url': 'https://images.unsplash.com/photo-1537996194471-e657df8fabcc?auto=format&fit=crop&q=80',
            },
        },
        {
            'title': 'Swiss Alpine Journey',
            'slug': 'swiss-alpine-journey',
            'country': 'Switzerland',
            'duration': '7 Days / 6 Nights',
            'price': '$1,299',
            'summary': 'Glacier trails, lake towns, and alpine villages across classic Switzerland.',
            'description': 'A scenic mountain trip with lakeside views, train journeys, and timeless alpine scenery.',
            'image': 'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&q=80',
            'is_popular': True,
            'destination': {
                'name': 'Swiss Alps',
                'country': 'Switzerland',
                'description': 'Snowy peaks, lakes, and scenic villages in the heart of Europe.',
                'image_url': 'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&q=80',
            },
        },
        {
            'title': 'Moroccan Heritage Tour',
            'slug': 'moroccan-heritage-tour',
            'country': 'Morocco',
            'duration': '6 Days / 5 Nights',
            'price': '$899',
            'summary': 'Wander medinas, architecture, desert light, and vibrant local culture.',
            'description': 'An immersive trip through colorful markets, historic streets, and beautiful desert landscapes.',
            'image': 'https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?auto=format&fit=crop&q=80',
            'is_popular': False,
            'destination': {
                'name': 'Marrakesh',
                'country': 'Morocco',
                'description': 'A vibrant city with markets, gardens, and historic architecture.',
                'image_url': 'https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?auto=format&fit=crop&q=80',
            },
        },
    ]

    for package_data in packages:
        destination_data = package_data.pop('destination')
        destination, _ = Destination.objects.get_or_create(
            name=destination_data['name'],
            defaults=destination_data,
        )
        TourPackage.objects.get_or_create(
            slug=package_data['slug'],
            defaults={
                **package_data,
                'destination': destination,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ('tour_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='contact_method',
            field=models.CharField(
                choices=[('whatsapp', 'WhatsApp'), ('email', 'Email'), ('phone', 'Phone Call')],
                default='whatsapp',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='booking',
            name='country',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='booking',
            name='guest_phone',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='booking',
            name='package_name',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AddField(
            model_name='booking',
            name='return_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='special_requests',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='booking',
            name='whatsapp_number',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.RunPython(seed_initial_packages, migrations.RunPython.noop),
    ]
