from django.db import migrations


def seed_tanzania_tours(apps, schema_editor):
    Destination = apps.get_model('tour_app', 'Destination')
    TourPackage = apps.get_model('tour_app', 'TourPackage')

    tours = [
        {
            'destination': {
                'name': 'Zanzibar',
                'country': 'Tanzania',
                'description': 'White-sand beaches, Stone Town, spice farms, and island adventures.',
                'image_url': 'https://images.unsplash.com/photo-1589979481223-deb893043163?auto=format&fit=crop&q=80',
            },
            'package': {
                'title': 'Zanzibar Beach Escape',
                'slug': 'zanzibar-beach-escape',
                'country': 'Tanzania',
                'duration': '5 Days / 4 Nights',
                'price': '$850',
                'summary': "Relax on Zanzibar's white-sand beaches.",
                'description': 'Includes airport transfer, hotel, Stone Town tour, spice tour, and beach activities.',
                'image': 'https://images.unsplash.com/photo-1589979481223-deb893043163?auto=format&fit=crop&q=80',
                'is_popular': True,
            },
        },
        {
            'destination': {
                'name': 'Serengeti National Park',
                'country': 'Tanzania',
                'description': 'World-famous wildlife safaris and the Great Migration.',
                'image_url': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&q=80',
            },
            'package': {
                'title': 'Serengeti Safari Adventure',
                'slug': 'serengeti-safari-adventure',
                'country': 'Tanzania',
                'duration': '4 Days / 3 Nights',
                'price': '$1,200',
                'summary': 'Experience wildlife in the Serengeti.',
                'description': 'A guided safari featuring game drives, accommodation, meals, and park fees.',
                'image': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&q=80',
                'is_popular': True,
            },
        },
        {
            'destination': {
                'name': 'Mount Kilimanjaro',
                'country': 'Tanzania',
                'description': "Africa's highest mountain and an unforgettable trekking experience.",
                'image_url': 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?auto=format&fit=crop&q=80',
            },
            'package': {
                'title': 'Kilimanjaro Trekking Expedition',
                'slug': 'kilimanjaro-trekking-expedition',
                'country': 'Tanzania',
                'duration': '7 Days / 6 Nights',
                'price': '$2,500',
                'summary': "Climb Africa's highest mountain.",
                'description': 'A guided Kilimanjaro climb with trained guides, porters, meals, permits, and camping equipment.',
                'image': 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?auto=format&fit=crop&q=80',
                'is_popular': True,
            },
        },
    ]

    for tour in tours:
        destination, _ = Destination.objects.get_or_create(
            name=tour['destination']['name'],
            defaults=tour['destination'],
        )
        TourPackage.objects.get_or_create(
            slug=tour['package']['slug'],
            defaults={**tour['package'], 'destination': destination},
        )


class Migration(migrations.Migration):
    dependencies = [('tour_app', '0002_booking_contact_method_booking_country_and_more')]

    operations = [migrations.RunPython(seed_tanzania_tours, migrations.RunPython.noop)]
