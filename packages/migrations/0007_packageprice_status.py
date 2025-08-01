# Generated by Django 5.2.4 on 2025-08-02 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0006_package_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='packageprice',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('close', 'Unavailable')], default='open', help_text='Availability status of the package on a specific date', max_length=15),
        ),
    ]
