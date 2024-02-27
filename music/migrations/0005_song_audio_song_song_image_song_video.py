# Generated by Django 5.0.2 on 2024-02-26 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_remove_song_audio_remove_song_song_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to='songs/audio/'),
        ),
        migrations.AddField(
            model_name='song',
            name='song_image',
            field=models.ImageField(blank=True, null=True, upload_to='songs/image/'),
        ),
        migrations.AddField(
            model_name='song',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='songs/video/'),
        ),
    ]