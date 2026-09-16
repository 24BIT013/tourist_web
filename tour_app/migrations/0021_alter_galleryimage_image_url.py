from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('tour_app', '0020_expand_tour_slug_length')]

    operations = [
        migrations.AlterField(
            model_name='galleryimage',
            name='image_url',
            field=models.CharField(
                help_text='Use a local image path beginning with images/.',
                max_length=500,
            ),
        ),
    ]
