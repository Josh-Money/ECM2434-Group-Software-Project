# Generated by Django 5.1.5 on 2025-03-23 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default_profile.jpg', upload_to='profile_pics'),
        ),
    ]
