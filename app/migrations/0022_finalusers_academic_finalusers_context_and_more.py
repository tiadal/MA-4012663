# Generated by Django 4.0.6 on 2022-08-28 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_rename_age_finalusers_age_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='finalusers',
            name='academic',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='finalusers',
            name='context',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='finalusers',
            name='occupation',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='finalusers',
            name='privacy',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]