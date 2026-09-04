from django.db import migrations


def add_zanzibar_island_tours_and_gallery_images(apps, schema_editor):
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

    tours = [
        {
            'title': 'Nakupenda Island Tour',
            'slug': 'nakupenda-island-tour',
            'country': 'Tanzania',
            'duration': 'Half Day',
            'price': '$100',
            'summary': 'Sail to Nakupenda Island for white sand, clear water, and relaxation.',
            'description': 'Enjoy a guided Nakupenda Island escape with time to swim, relax on the sandbank, and take in Zanzibar’s turquoise Indian Ocean views.',
            'image': 'images/tours/nakupenda.png',
            'is_popular': True,
        },
        {
            'title': 'Prison Island Zanzibar Tour',
            'slug': 'prison-island-zanzibar-tour',
            'country': 'Tanzania',
            'duration': 'Half Day',
            'price': '$100',
            'summary': 'Discover Prison Island’s history, giant tortoises, and coastal scenery.',
            'description': 'Travel by boat to Prison Island and explore its historic buildings, meet the giant tortoises, and enjoy free time beside the clear Zanzibar sea.',
            'image': 'images/tours/kobe.png',
            'is_popular': True,
        },
        {
            'title': 'Stone Town Zanzibar Tour',
            'slug': 'stone-town-zanzibar-tour',
            'country': 'Tanzania',
            'duration': 'Half Day',
            'price': '$100',
            'summary': 'Walk through Stone Town’s historic lanes, markets, and Swahili culture.',
            'description': 'Explore Zanzibar’s UNESCO-listed Stone Town with a local guide, visiting its winding streets, landmark architecture, markets, and cultural stories.',
            'image': 'images/tours/hamn.png',
            'is_popular': True,
        },
    ]
    for tour in tours:
        TourPackage.objects.update_or_create(
            slug=tour['slug'], defaults={**tour, 'destination': zanzibar}
        )

    gallery_images = [
        {
            'title': 'Kongwe Beach',
            'image_url': 'images/gallery/kongwe.png',
            'caption': 'A peaceful Zanzibar beach moment at Kongwe.',
        },
        {
            'title': 'Stone Town Zanzibar',
            'image_url': 'images/gallery/hamn.png',
            'caption': 'Stone Town’s distinctive historic character and coastal culture.',
        },
        {
            'title': 'Prison Island Zanzibar',
            'image_url': 'images/gallery/kobe.png',
            'caption': 'A memorable Prison Island visit in Zanzibar.',
        },
        {
            'title': 'Nakupenda Island',
            'image_url': 'images/gallery/nakupenda.png',
            'caption': 'Beautiful sand and clear sea at Nakupenda Island.',
        },
    ]
    for image in gallery_images:
        GalleryImage.objects.update_or_create(image_url=image['image_url'], defaults=image)


class Migration(migrations.Migration):
    dependencies = [('tour_app', '0010_complaint')]

    operations = [migrations.RunPython(add_zanzibar_island_tours_and_gallery_images, migrations.RunPython.noop)]
