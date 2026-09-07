from django.db import migrations


def add_all_tour_images_to_gallery(apps, schema_editor):
    GalleryImage = apps.get_model('tour_app', 'GalleryImage')

    photos = [
        {
            'title': 'Nakupenda Sandbank',
            'image_url': 'images/gallery/nakupenda.png',
            'caption': 'Escape to Nakupenda Sandbank, a brilliant stretch of white sand surrounded by clear turquoise water. Swim, relax in the warm Indian Ocean, enjoy the open sea views, and capture the peaceful beauty that makes this Zanzibar stop unforgettable.',
        },
        {
            'title': 'Prison Island',
            'image_url': 'images/gallery/kobe.png',
            'caption': 'Visit Prison Island by boat to discover its rich history, coastal scenery, and famous giant Aldabra tortoises. Explore the island at a relaxed pace, learn about its past, and enjoy time beside the clear waters just off Stone Town.',
        },
        {
            'title': 'Stone Town Zanzibar',
            'image_url': 'images/gallery/hamn.png',
            'caption': 'Step into the winding lanes of Stone Town, where carved doors, lively markets, historic buildings, and oceanfront views tell Zanzibar’s Swahili story. This image captures the culture and character of the island’s UNESCO-listed old town.',
        },
        {
            'title': 'Ngome Kongwe, the Old Fort',
            'image_url': 'images/gallery/kongwe.png',
            'caption': 'See Ngome Kongwe, Zanzibar’s historic Old Fort, in the heart of Stone Town. Its strong coral-stone walls, open courtyard, and surrounding cultural life offer a vivid glimpse into the island’s Omani, Swahili, and trading heritage.',
        },
        {
            'title': 'Unguja Ukuu Snorkeling',
            'image_url': 'images/tours/sn.jpg',
            'caption': 'Dive into the clear coastal waters of Unguja Ukuu for a relaxed snorkeling adventure. Watch for colourful fish and marine life beneath the surface, then enjoy the calm sea, warm sunshine, and beautiful south-Zanzibar shoreline.',
        },
        {
            'title': 'Zanzibar Sunset Dhow Cruise',
            'image_url': 'images/tours/sun.png',
            'caption': 'Sail along Zanzibar’s coast on a traditional wooden dhow as the sky turns gold, orange, and pink. The gentle sea breeze, rhythmic waves, and sunset horizon create a peaceful and memorable evening on the Indian Ocean.',
        },
        {
            'title': 'Clear Kayaking in Zanzibar',
            'image_url': 'images/tours/zanzibar-clear-kayak.png',
            'caption': 'Paddle through Zanzibar’s calm, transparent water in a clear kayak and enjoy a unique view beneath you. This gentle experience is perfect for taking photographs, spotting the seabed, and soaking up the island’s bright coastal scenery.',
        },
        {
            'title': 'Zanzibar Spice Farm Experience',
            'image_url': 'images/tours/sp.png',
            'caption': 'Discover why Zanzibar is called the Spice Island during a visit to a working spice farm. Smell fresh cloves, cinnamon, vanilla, and tropical fruit while learning how these plants are grown, harvested, and used in local Swahili cooking.',
        },
        {
            'title': 'Zanzibar Kayaking Adventure',
            'image_url': 'images/tours/zanzibar-clear-kayak.png',
            'caption': 'Glide across Zanzibar’s quiet lagoon waters by kayak, surrounded by blue sea, coastal light, and the gentle rhythm of the tide. It is an easy-going way to explore the shoreline and appreciate the island from the water.',
        },
        {
            'title': 'Zanzibar Quad Biking',
            'image_url': 'images/tours/quad-biking-in-zanzibar.png',
            'caption': 'Travel beyond the beach on a guided quad-bike ride through Zanzibar’s countryside, village routes, and palm-lined tracks. The adventure combines exciting off-road riding with a closer look at the island’s everyday landscapes and local communities.',
        },
        {
            'title': 'Zanzibar Spice Farm Tour',
            'image_url': 'images/tours/spice-farm-zanzibar.png',
            'caption': 'Walk among aromatic spice plants and tropical fruit trees with a local guide at a Zanzibar spice farm. Learn the stories behind the island’s famous harvest, taste fresh seasonal ingredients, and experience the colour and fragrance of rural Zanzibar.',
        },
        {
            'title': 'Nakupenda Island Tour',
            'image_url': 'images/tours/nakupenda.png',
            'caption': 'Enjoy the soft white sand and sparkling sea of Nakupenda, a beloved Zanzibar sandbank escape. There is time to swim, relax, take photographs, and enjoy a beautiful day surrounded by the open Indian Ocean.',
        },
        {
            'title': 'Prison Island Zanzibar Tour',
            'image_url': 'images/tours/kobe.png',
            'caption': 'Take a memorable boat trip to Prison Island, where historic ruins and giant tortoises sit alongside clear blue water. The island is a wonderful mix of Zanzibar history, wildlife, and peaceful coastal scenery.',
        },
        {
            'title': 'Stone Town Walking Tour',
            'image_url': 'images/tours/hamn.png',
            'caption': 'Explore Stone Town’s atmospheric streets, historic architecture, and bustling local corners with a guide. Every turn reveals another layer of Zanzibar’s culture, from carved wooden doors to stories of trade, music, and the sea.',
        },
    ]

    for photo in photos:
        GalleryImage.objects.update_or_create(image_url=photo['image_url'], defaults=photo)


class Migration(migrations.Migration):
    dependencies = [('tour_app', '0015_replace_ngome_kongwe_with_spice_prison_stone_town_tour')]

    operations = [migrations.RunPython(add_all_tour_images_to_gallery, migrations.RunPython.noop)]
