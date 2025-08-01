# Generated by Django 5.2.4 on 2025-07-31 08:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0004_packageprice'),
        ('room_types', '0006_alter_roomtype_accommodation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='room_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='room_types.roomtype'),
        ),
        migrations.AlterField(
            model_name='packageprice',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_prices', to='packages.package'),
        ),
    ]
