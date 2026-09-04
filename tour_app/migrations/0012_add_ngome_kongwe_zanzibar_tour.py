from django.db import migrations


def add_ngome_kongwe_zanzibar_tour(apps, schema_editor):
    Destination = apps.get_model('tour_app', 'Destination')
    GalleryImage = apps.get_model('tour_app', 'GalleryImage')
    TourPackage = apps.get_model('tour_app', 'TourPackage')

    zanzibar, _ = Destination.objects.get_or_create(
        name='Zanzibar',
        defaults={
            'country': 'Tanzania',
            'description': 'White-sand beaches, Stone Town, spice farms, and island adventures.',
        },
    )

    TourPackage.objects.update_or_create(
        slug='ngome-kongwe-zanzibar-tour',
        defaults={
            'title': 'Ngome Kongwe Zanzibar Tour',
            'destination': zanzibar,
            'country': 'Tanzania',
            'duration': 'Half Day',
            'price': '$100',
            'summary': 'Discover the stories, architecture, and ocean views of Zanzibar’s historic Ngome Kongwe.',
            'description': (
                'Step inside Ngome Kongwe, also known as the Old Fort, one of Stone Town’s most important historic '
                'landmarks. Your local guide will introduce the fort’s origins, its role in Zanzibar’s Omani and '
                'Swahili history, and the cultural life that continues around its stone walls today. Walk through the '
                'courtyard and restored spaces, hear stories of trade, defence, and island heritage, then continue '
                'through nearby Stone Town lanes for views of carved doors, busy local streets, and the waterfront. '
                'This relaxed half-day experience is ideal for visitors who want a meaningful introduction to '
                'Zanzibar’s history, culture, and architectural character.'
            ),
            'image': 'images/tours/kongwe.png',
            'is_popular': True,
        },
    )

    GalleryImage.objects.update_or_create(
        image_url='images/gallery/kongwe.png',
        defaults={
            'title': 'Ngome Kongwe Zanzibar',
            'caption': 'Explore Ngome Kongwe, Zanzibar’s historic Old Fort in the heart of Stone Town.',
        },
    )


class Migration(migrations.Migration):
    dependencies = [('tour_app', '0011_add_zanzibar_island_tours_and_gallery_images')]

    operations = [migrations.RunPython(add_ngome_kongwe_zanzibar_tour, migrations.RunPython.noop)]
