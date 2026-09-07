from django.db import migrations


def add_zanzibar_full_day_and_sea_tours(apps, schema_editor):
    Destination = apps.get_model('tour_app', 'Destination')
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
            'title': 'Unguja Ukuu Snorkeling Tour',
            'slug': 'unguja-ukuu-snorkeling-tour',
            'duration': 'Half Day',
            'price': '$100',
            'summary': 'Snorkel the clear, colourful waters around the historic village of Unguja Ukuu.',
            'description': 'Set out for a relaxed Unguja Ukuu snorkeling experience with time to swim above colourful marine life and enjoy Zanzibar’s warm Indian Ocean waters.',
            'image': 'images/tours/sn.jpg',
        },
        {
            'title': 'Sunset Dhow Cruise in Zanzibar',
            'slug': 'sunset-dhow-cruise-in-zanzibar',
            'duration': 'Evening',
            'price': '$100',
            'summary': 'Sail Zanzibar’s coast on a traditional dhow as the sun sets over the ocean.',
            'description': 'Unwind aboard a traditional dhow cruise and take in the golden Zanzibar sunset, gentle sea breeze, and beautiful coastal views.',
            'image': 'images/tours/sun.png',
        },
        {
            'title': 'Nakupenda Sandbank, Prison Island & Stone Town',
            'slug': 'nakupenda-prison-island-stone-town-full-day-tour',
            'duration': 'Full Day',
            'price': '$180',
            'summary': 'A complete day of sandbank swimming, Prison Island history, and Stone Town culture.',
            'description': 'Spend a full day visiting Nakupenda Sandbank, Prison Island, and Stone Town. Swim in clear water, meet giant tortoises, and explore the historic heart of Zanzibar with a local guide.',
            'image': 'images/tours/nakupenda.png',
        },
        {
            'title': 'Sunset Dhow, Unguja Ukuu Snorkeling & Kayaking',
            'slug': 'sunset-dhow-unguja-ukuu-snorkeling-kayaking-full-day-tour',
            'duration': 'Full Day',
            'price': '$180',
            'summary': 'A sea-loving full day of snorkeling, clear kayaking, and a sunset dhow cruise.',
            'description': 'Enjoy a full day on and around the water: snorkel at Unguja Ukuu, paddle a clear kayak, then finish with a memorable Zanzibar sunset dhow cruise.',
            'image': 'images/tours/sn.jpg',
        },
        {
            'title': 'Spice Farm & Prison Island Tour',
            'slug': 'spice-farm-prison-island-full-day-tour',
            'duration': 'Full Day',
            'price': '$160',
            'summary': 'Combine Zanzibar’s fragrant spice farms with Prison Island’s famous tortoises.',
            'description': 'Discover the aromas and stories of a Zanzibar spice farm before travelling to Prison Island to visit giant tortoises, historic ruins, and clear coastal waters.',
            'image': 'images/tours/sp.png',
        },
    ]

    for tour in tours:
        TourPackage.objects.update_or_create(
            slug=tour['slug'],
            defaults={**tour, 'destination': zanzibar, 'country': 'Tanzania', 'is_popular': True},
        )


class Migration(migrations.Migration):
    dependencies = [('tour_app', '0013_transportbooking')]

    operations = [migrations.RunPython(add_zanzibar_full_day_and_sea_tours, migrations.RunPython.noop)]
