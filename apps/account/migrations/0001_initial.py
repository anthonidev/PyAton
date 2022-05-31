# Generated by Django 4.0.4 on 2022-05-31 04:55

import cloudinary.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('treatment', models.CharField(choices=[('Sr.', 'Sr.'), ('Sra.', 'Sra.')], default='Sr.', max_length=4)),
                ('photo', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='Image')),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('dob', models.DateField(default=datetime.datetime.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('enterprise', models.CharField(default='', max_length=255)),
                ('address', models.CharField(default='', max_length=255)),
                ('zipcode', models.CharField(default='', max_length=20)),
                ('district', models.CharField(default='', max_length=255)),
                ('city', models.CharField(choices=[('Amazonas', 'Amazonas'), ('Áncash', 'Áncash'), ('Apurímac', 'Apurímac'), ('Arequipa', 'Arequipa'), ('Ayacucho', 'Ayacucho'), ('Cajamarca', 'Cajamarca'), ('Callao', 'Callao'), ('Cusco', 'Cusco'), ('Huancavelica', 'Huancavelica'), ('Huánuco', 'Huánuco'), ('Ica', 'Ica'), ('Junín', 'Junín'), ('La Libertad', 'Lalibertad'), ('Lambayeque', 'Lambayeque'), ('Lima', 'Lima'), ('Loreto', 'Loreto'), ('Madre de Dios', 'Madrededios'), ('Moquegua', 'Moquegua'), ('Pasco', 'Pasco'), ('Piura', 'Piura'), ('Puno', 'Puno'), ('San Martín', 'Sanmartín'), ('Tacna', 'Tacna'), ('Tumbes', 'Tumbes'), ('Ucayali', 'Ucayali')], default='Lima', max_length=255)),
                ('phone', models.CharField(default='', max_length=255)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.userprofile')),
            ],
        ),
    ]
