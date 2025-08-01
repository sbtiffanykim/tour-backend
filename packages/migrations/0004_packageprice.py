# Generated by Django 5.2.4 on 2025-07-31 07:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0003_alter_package_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackagePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('price', models.PositiveIntegerField(help_text='daily price')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_price', to='packages.package')),
            ],
            options={
                'unique_together': {('package', 'date')},
            },
        ),
    ]
