# Generated by Django 5.0.2 on 2024-03-06 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('colab', '0003_remove_colab_colab_description_colab_colab_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colab',
            name='audio',
            field=models.URLField(),
        ),
    ]