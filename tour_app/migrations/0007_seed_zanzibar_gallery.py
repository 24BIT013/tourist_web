from django.db import migrations


def seed_zanzibar_gallery(apps, schema_editor):
    GalleryImage = apps.get_model('tour_app', 'GalleryImage')
    photos = [
        {
            'title': 'Clear Kayaking Through Zanzibar Mangroves',
            'image_url': 'images/tours/zanzibar-clear-kayak.png',
            'caption': (
                'Glide across Zanzibar’s clear, shallow waters in a transparent kayak and enjoy views of the '
                'mangrove roots and marine life below. This peaceful half-day experience is ideal for couples, '
                'families, and anyone who wants to explore the island’s coastal nature with a local guide.'
            ),
        },
        {
            'title': 'Zanzibar Spice Farm Experience',
            'image_url': 'images/tours/spice-farm-zanzibar.png',
            'caption': (
                'Visit a traditional Zanzibar spice farm to discover why the island is known as the Spice Island. '
                'Learn how cloves, cinnamon, vanilla, cardamom, tropical fruit, and herbs are grown, then enjoy '
                'the aromas, stories, and fresh tastes shared by local farmers.'
            ),
        },
        {
            'title': 'Quad Biking Across Zanzibar',
            'image_url': 'images/tours/quad-biking-in-zanzibar.png',
            'caption': (
                'Take an exciting quad bike ride through Zanzibar’s countryside, passing village paths, open '
                'landscapes, and island scenery. Your guided adventure combines off-road fun with a closer look '
                'at everyday local life beyond the beach.'
            ),
        },
    ]
    for photo in photos:
        GalleryImage.objects.get_or_create(image_url=photo['image_url'], defaults=photo)


class Migration(migrations.Migration):
    dependencies = [('tour_app', '0006_use_zanzibar_tour_images')]

    operations = [
        migrations.RunPython(seed_zanzibar_gallery, migrations.RunPython.noop),
    ]
