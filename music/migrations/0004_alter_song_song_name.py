# Generated by Django 5.0.2 on 2024-02-27 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_rename_song_image_song_song_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='song_name',
            field=models.CharField(max_length=500, unique=True),
        ),
    ]
