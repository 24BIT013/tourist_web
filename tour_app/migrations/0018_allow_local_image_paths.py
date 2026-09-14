from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour_app', '0017_add_feature_photos_and_remove_gallery_duplicates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galleryimage',
            name='image_url',
            field=models.CharField(help_text='Use a public link or a local path beginning with images/.', max_length=500),
        ),
        migrations.AlterField(
            model_name='tourpackage',
            name='image',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
