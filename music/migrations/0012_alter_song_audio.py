# Generated by Django 5.0.2 on 2024-03-06 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0011_alter_recentsongs_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='audio',
            field=models.URLField(),
        ),
    ]
