# Generated by Django 5.0.2 on 2024-02-26 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0006_alter_albuminplaylist_album_id_alter_song_album_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='album_picture',
            field=models.ImageField(blank=True, null=True, upload_to='album/images/'),
        ),
    ]