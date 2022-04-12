# Generated by Django 2.2.16 on 2022-04-12 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220412_1826'),
    ]

    operations = [
        migrations.RenameField(
            model_name='title',
            old_name='categories',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='title',
            old_name='genres',
            new_name='genre',
        ),
        migrations.AddField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]