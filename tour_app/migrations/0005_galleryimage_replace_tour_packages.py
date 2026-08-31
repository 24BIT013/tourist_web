from django.db import migrations, models


def replace_tour_packages(apps, schema_editor):
    Destination = apps.get_model('tour_app', 'Destination')
    TourPackage = apps.get_model('tour_app', 'TourPackage')

    # A fresh set of Zanzibar day tours replaces every previous package.
    # Existing bookings are retained; their package link becomes empty because
    # the Booking model uses SET_NULL for deleted packages.
    TourPackage.objects.all().delete()
    zanzibar, _ = Destination.objects.get_or_create(
        name='Zanzibar',
        defaults={
            'country': 'Tanzania',
            'description': 'Island adventures, spice farms, mangroves, and coastal experiences.',
        },
    )

    tours = [
        {
            'title': 'Kayaking Through Mangroves in Zanzibar',
            'slug': 'kayaking-through-mangroves-in-zanzibar',
            'duration': 'Half Day',
            'price': '$100',
            'summary': 'Paddle through Zanzibar’s peaceful mangrove channels with a local guide.',
            'description': 'Discover the calm beauty of Zanzibar’s mangrove forests on a guided kayaking adventure.',
            'image': 'https://images.unsplash.com/photo-1502680390469-be75c86b636f?auto=format&fit=crop&q=80',
        },
        {
            'title': 'Spice Farm Tour in Zanzibar',
            'slug': 'spice-farm-tour-in-zanzibar',
            'duration': 'Half Day',
            'price': '$110',
            'summary': 'See, smell, and taste the spices that make Zanzibar famous.',
            'description': 'Visit a traditional spice farm and learn about the island’s fragrant herbs, fruits, and spices.',
            'image': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&q=80',
        },
        {
            'title': 'Quad Bikes Tour in Zanzibar',
            'slug': 'quad-bikes-tour-in-zanzibar',
            'duration': 'Half Day',
            'price': '$120',
            'summary': 'Ride quad bikes through Zanzibar’s scenic villages and countryside.',
            'description': 'Enjoy a guided quad bike tour that combines adventure, local culture, and island scenery.',
            'image': 'https://images.unsplash.com/photo-1591825729269-caeb344f6df2?auto=format&fit=crop&q=80',
        },
    ]
    for tour in tours:
        TourPackage.objects.create(destination=zanzibar, country='Tanzania', is_popular=True, **tour)


class Migration(migrations.Migration):
    dependencies = [('tour_app', '0004_booking_total_price')]

    operations = [
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150)),
                ('image_url', models.URLField(help_text='Paste the public link to the photograph.')),
                ('caption', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'gallery image',
                'verbose_name_plural': 'gallery images',
                'ordering': ('-created_at',),
            },
        ),
        migrations.RunPython(replace_tour_packages, migrations.RunPython.noop),
    ]
