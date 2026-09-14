from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('tour_app', '0018_allow_local_image_paths')]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='image_url',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='transportbooking',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
    ]
