# Generated by Django 5.0.2 on 2024-02-26 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0009_remove_album_album_picture_url_album_album_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='album_picture',
            field=models.URLField(blank=True, null=True),
        ),
    ]