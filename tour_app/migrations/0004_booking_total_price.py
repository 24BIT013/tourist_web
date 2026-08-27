from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour_app', '0003_seed_tanzania_tours'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='total_price',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
