# Generated by Django 4.0.4 on 2022-06-08 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0003_alter_wishlistitem_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='total_items',
        ),
    ]