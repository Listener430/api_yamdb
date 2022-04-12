# Generated by Django 2.2.16 on 2022-04-12 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20220412_2144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genrestitle',
            name='genres',
        ),
        migrations.AddField(
            model_name='genrestitle',
            name='genre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='reviews.Genre'),
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, help_text='Категория, к которой будет относиться произведение', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='titles', to='reviews.Category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(related_name='titles', through='reviews.GenresTitle', to='reviews.Genre'),
        ),
    ]
