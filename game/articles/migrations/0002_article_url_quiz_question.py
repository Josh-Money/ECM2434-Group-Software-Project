# Generated by Django 5.1.5 on 2025-03-18 15:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='url',
            field=models.URLField(blank=True, help_text='Optional external URL to article content', null=True),
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('points_per_question', models.PositiveIntegerField(default=10, help_text='Points awarded per correct answer')),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='articles.article')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('correct_answer', models.CharField(choices=[('true', 'True'), ('false', 'False')], max_length=10)),
                ('order', models.PositiveIntegerField(default=0, help_text='Order of question in the quiz')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='articles.quiz')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
