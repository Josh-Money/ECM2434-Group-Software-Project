# Generated by Django 5.1.6 on 2025-03-08 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0003_alter_leaderboard_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaderboard',
            name='activity_type',
            field=models.CharField(choices=[('main', 'Main'), ('qr_scan', 'QR Scan'), ('quiz', 'Article Quiz'), ('travel', 'Travel Log')], max_length=10),
        ),
    ]
