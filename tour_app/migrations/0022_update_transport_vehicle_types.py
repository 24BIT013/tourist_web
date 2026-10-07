from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('tour_app', '0021_alter_galleryimage_image_url'),
    ]

    def update_vehicle_types(apps, schema_editor):
        TransportBooking = apps.get_model('tour_app', 'TransportBooking')
        TransportBooking.objects.filter(vehicle_type__in=['car', 'suv']).update(vehicle_type='private')
        TransportBooking.objects.filter(vehicle_type='van').update(vehicle_type='minibus')

    def restore_vehicle_types(apps, schema_editor):
        TransportBooking = apps.get_model('tour_app', 'TransportBooking')
        TransportBooking.objects.filter(vehicle_type='private').update(vehicle_type='car')
        TransportBooking.objects.filter(vehicle_type='minibus').update(vehicle_type='van')

    operations = [
        migrations.RunPython(update_vehicle_types, restore_vehicle_types),
        migrations.AlterField(
            model_name='transportbooking',
            name='vehicle_type',
            field=models.CharField(
                choices=[('private', 'Private'), ('minibus', 'Minibus')],
                default='private',
                max_length=20,
            ),
        ),
    ]
