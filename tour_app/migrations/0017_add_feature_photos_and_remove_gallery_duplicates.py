from django.db import migrations


def update_gallery(apps, schema_editor):
    GalleryImage = apps.get_model('tour_app', 'GalleryImage')

    # These files are byte-for-byte copies of photos already displayed from
    # the gallery folder, so retain the original gallery entry only.
    duplicate_urls = [
        'images/tours/zanzibar-clear-kayak.png',
        'images/tours/quad-biking-in-zanzibar.png',
        'images/tours/spice-farm-zanzibar.png',
        'images/tours/nakupenda.png',
        'images/tours/kobe.png',
        'images/tours/hamn.png',
    ]
    GalleryImage.objects.filter(image_url__in=duplicate_urls).delete()

    photos = [
        {
            'title': 'Zanzibar Coastal Moment',
            'image_url': 'images/foro.png',
            'caption': 'Take in one of Zanzibar’s beautiful coastal moments, where the blue Indian Ocean, warm island light, and relaxed shoreline atmosphere invite you to slow down. It is a wonderful reminder of the natural beauty waiting between every island adventure.',
        },
        {
            'title': 'Zanzibar Island Experience',
            'image_url': 'images/gallery/pesa.jpg',
            'caption': 'Discover another side of Zanzibar through this island experience, filled with local colour, tropical scenery, and the easy-going spirit of travel. Every visit offers time to make memories, meet welcoming people, and enjoy the details that make Zanzibar special.',
        },
        {
            'title': 'Zanzibar Ocean Escape',
            'image_url': 'images/tau.png',
            'caption': 'Enjoy Zanzibar’s inviting ocean scenery, where clear water and coastal views create the perfect setting for a day of exploration or quiet relaxation. From sunrise to sunset, the island’s shore is full of beautiful places to pause, breathe, and take photographs.',
        },
        {
            'title': 'Zanzibar Adventure View',
            'image_url': 'images/saaa.png',
            'caption': 'See Zanzibar through the lens of adventure: vibrant landscapes, tropical light, and moments that connect visitors with the island’s beaches, culture, and nature. This image celebrates the relaxed but unforgettable spirit of a Zanzibar holiday.',
        },
    ]

    for photo in photos:
        GalleryImage.objects.update_or_create(image_url=photo['image_url'], defaults=photo)


class Migration(migrations.Migration):
    dependencies = [('tour_app', '0016_add_all_tour_images_to_gallery')]

    operations = [migrations.RunPython(update_gallery, migrations.RunPython.noop)]
