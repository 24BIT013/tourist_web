from django.db import migrations


def use_uploaded_gallery_photos(apps, schema_editor):
    GalleryImage = apps.get_model('tour_app', 'GalleryImage')
    photos = [
        {
            'old_url': 'images/tours/zanzibar-clear-kayak.png',
            'title': 'Clear Kayaking in Zanzibar',
            'image_url': 'images/gallery/kayaking.jpg',
            'caption': 'Explore Zanzibar’s calm coastal waters from a clear kayak.',
        },
        {
            'old_url': 'images/tours/quad-biking-in-zanzibar.png',
            'title': 'Quad Biking Adventure',
            'image_url': 'images/gallery/quad.jpg',
            'caption': 'Discover Zanzibar’s countryside on an exciting guided quad ride.',
        },
        {
            'old_url': 'images/tours/spice-farm-zanzibar.png',
            'title': 'Zanzibar Spice Farm',
            'image_url': 'images/gallery/spice.jpg',
            'caption': 'Experience the colours, aromas, and flavours of Zanzibar’s spice farms.',
        },
    ]
    for photo in photos:
        old_url = photo.pop('old_url')
        existing = GalleryImage.objects.filter(image_url=old_url).first()
        if existing:
            for field, value in photo.items():
                setattr(existing, field, value)
            existing.save(update_fields=['title', 'image_url', 'caption'])
        else:
            GalleryImage.objects.get_or_create(image_url=photo['image_url'], defaults=photo)


class Migration(migrations.Migration):
    dependencies = [('tour_app', '0007_seed_zanzibar_gallery')]

    operations = [
        migrations.RunPython(use_uploaded_gallery_photos, migrations.RunPython.noop),
    ]
