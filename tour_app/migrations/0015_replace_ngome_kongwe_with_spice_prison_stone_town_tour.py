from django.db import migrations


def replace_tours(apps, schema_editor):
    TourPackage = apps.get_model('tour_app', 'TourPackage')

    # Bookings retain their saved package name when this retired tour is removed.
    TourPackage.objects.filter(slug='ngome-kongwe-zanzibar-tour').delete()

    TourPackage.objects.filter(slug='spice-farm-prison-island-full-day-tour').update(
        title='Spice Farm, Prison Island and Stone Town Zanzibar Tour',
        summary='A full-day journey through Zanzibar’s spice farms, Prison Island, and historic Stone Town.',
        description=(
            'Explore Zanzibar in one memorable day: discover fragrant spices at a local farm, visit the giant '
            'tortoises and historic ruins of Prison Island, then wander the distinctive streets and landmarks of '
            'Stone Town with a local guide.'
        ),
    )


class Migration(migrations.Migration):
    dependencies = [('tour_app', '0014_add_zanzibar_full_day_and_sea_tours')]

    operations = [migrations.RunPython(replace_tours, migrations.RunPython.noop)]
