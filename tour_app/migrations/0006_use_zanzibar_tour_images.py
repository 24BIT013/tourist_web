from django.db import migrations


def use_zanzibar_tour_images(apps, schema_editor):
    TourPackage = apps.get_model('tour_app', 'TourPackage')
    images = {
        'kayaking-through-mangroves-in-zanzibar': 'images/tours/zanzibar-clear-kayak.png',
        'spice-farm-tour-in-zanzibar': 'images/tours/spice-farm-zanzibar.png',
        'quad-bikes-tour-in-zanzibar': 'images/tours/quad-biking-in-zanzibar.png',
    }
    for slug, image in images.items():
        TourPackage.objects.filter(slug=slug).update(image=image)


class Migration(migrations.Migration):
    dependencies = [('tour_app', '0005_galleryimage_replace_tour_packages')]

    operations = [
        migrations.RunPython(use_zanzibar_tour_images, migrations.RunPython.noop),
    ]
