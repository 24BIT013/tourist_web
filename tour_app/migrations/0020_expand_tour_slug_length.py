from django.db import migrations, models


OLD_SLUG = 'sunset-dhow-unguja-ukuu-snorkeling-kayaking-full-day-tour'
NEW_SLUG = 'sunset-dhow-unguja-ukuu-snorkeling-kayaking-tour'


def rename_oversized_seed_slug(apps, schema_editor):
    TourPackage = apps.get_model('tour_app', 'TourPackage')
    TourPackage.objects.filter(slug=OLD_SLUG).update(slug=NEW_SLUG)


class Migration(migrations.Migration):
    dependencies = [('tour_app', '0019_destination_image_path_and_transport_status')]

    operations = [
        migrations.AlterField(
            model_name='tourpackage',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
        migrations.RunPython(rename_oversized_seed_slug, migrations.RunPython.noop),
    ]
