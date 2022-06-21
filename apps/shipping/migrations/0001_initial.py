# Generated by Django 4.0.4 on 2022-06-20 00:03

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='Image')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('time_to_delivery', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'verbose_name': 'Shipping',
                'verbose_name_plural': 'Shipping',
            },
        ),
    ]
