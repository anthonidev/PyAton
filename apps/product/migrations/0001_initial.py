# Generated by Django 4.0.4 on 2022-06-22 20:25

import cloudinary.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('photo', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='Image')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='product.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('compare_price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
                ('date_added', models.DateTimeField(default=datetime.datetime.now)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
                ('num_visits', models.IntegerField(default=0)),
                ('last_visit', models.DateTimeField(blank=True, null=True)),
                ('sold', models.IntegerField(default=0)),
                ('photo', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Image')),
                ('photo_thumbnail_sm', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='photo_thumbnail_sm')),
                ('photo_thumbnail_xm', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='photo_thumbnail_xm')),
                ('description', models.TextField(blank=True, null=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='product.category')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='colors', to='product.product')),
            ],
            options={
                'ordering': ('-date_added',),
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Image')),
                ('photo_thumbnail_sm', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='photo_thumbnail_sm')),
                ('photo_thumbnail_xm', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='photo_thumbnail_xm')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='CharacteristicProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristics', to='product.product')),
            ],
        ),
    ]