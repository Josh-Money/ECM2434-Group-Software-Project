# Generated by Django 5.1.5 on 2025-03-23 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='images/profile_pics/default_profile.jpg', null=True, upload_to='profile_pics'),
        ),
    ]
