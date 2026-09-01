from django.db import migrations


def expand_gallery(apps, schema_editor):
    GalleryImage = apps.get_model('tour_app', 'GalleryImage')
    photos = [
        {
            'title': 'Clear Kayaking in Zanzibar',
            'image_url': 'images/gallery/kayaking.jpg',
            'caption': (
                'Set out across Zanzibar’s warm, crystal-clear water in a transparent kayak, where every paddle '
                'stroke reveals shifting shades of blue and the sea life beneath you. Your guide shares local '
                'stories, points out the mangroves and calm channels, and gives you time to slow down, take '
                'photographs, and enjoy the coastline at an easy pace.'
            ),
        },
        {
            'title': 'Quad Biking Adventure',
            'image_url': 'images/gallery/quad.jpg',
            'caption': (
                'Leave the busy beach roads behind on a guided quad-bike journey through Zanzibar’s villages, '
                'palm-lined tracks, and open countryside. This energetic excursion combines off-road fun with '
                'meaningful stops along the route, giving you a closer look at local life, island landscapes, '
                'and the welcoming communities beyond the coast.'
            ),
        },
        {
            'title': 'Zanzibar Spice Farm',
            'image_url': 'images/gallery/spice.jpg',
            'caption': (
                'Follow the rich scents of cloves, cinnamon, vanilla, cardamom, and tropical fruit through a '
                'working Zanzibar spice farm. Local farmers explain how each plant is grown and used, then invite '
                'you to touch, smell, and taste the island’s famous harvest. It is a colourful, hands-on way to '
                'discover why Zanzibar is known around the world as the Spice Island.'
            ),
        },
        {
            'title': 'Mangrove Lagoon Kayak',
            'image_url': 'images/gallery/clear-kayak-lagoon.png',
            'caption': (
                'Drift quietly through a sheltered lagoon where mangrove roots meet the clear Indian Ocean. The '
                'clear kayak gives every guest a close view of the water below, while the peaceful route is ideal '
                'for couples, families, and first-time paddlers. Bring your camera for bright reflections, calm '
                'water, and the gentle coastal scenery that makes this Zanzibar moment unforgettable.'
            ),
        },
        {
            'title': 'Zanzibar Countryside Quad Ride',
            'image_url': 'images/gallery/quad-village-route.png',
            'caption': (
                'This guided quad route follows dusty island paths through green fields and village surroundings, '
                'with plenty of time to enjoy the changing scenery. It is more than a ride: you will see a quieter '
                'side of Zanzibar, learn from your local guide, and make memorable stops before returning with '
                'stories, photographs, and a real sense of adventure.'
            ),
        },
        {
            'title': 'Spice Farm Harvest',
            'image_url': 'images/gallery/spice-farm-harvest.png',
            'caption': (
                'Step into the heart of Zanzibar’s farming tradition and see the herbs, roots, and fruits that '
                'shape the island’s cooking and culture. During the visit, you can learn how spices are picked, '
                'how they are prepared, and which flavours are used in everyday Swahili dishes. The experience '
                'ends with the vivid colours and fragrant memories of a true Zanzibar spice-farm day.'
            ),
        },
    ]

    for photo in photos:
        GalleryImage.objects.update_or_create(image_url=photo['image_url'], defaults=photo)


class Migration(migrations.Migration):
    dependencies = [('tour_app', '0008_use_uploaded_gallery_photos')]

    operations = [migrations.RunPython(expand_gallery, migrations.RunPython.noop)]
