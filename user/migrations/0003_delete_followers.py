# Generated by Django 5.0.2 on 2024-02-28 04:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_avatar'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Followers',
        ),
    ]
