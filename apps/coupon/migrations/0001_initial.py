# Generated by Django 4.0.4 on 2022-06-22 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('value', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('num_available', models.IntegerField(default=10)),
                ('num_used', models.IntegerField(default=0)),
            ],
        ),
    ]
