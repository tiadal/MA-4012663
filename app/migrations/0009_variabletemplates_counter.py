# Generated by Django 4.0.6 on 2022-08-24 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_variabletemplates_language_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='variabletemplates',
            name='counter',
            field=models.IntegerField(default=0),
        ),
    ]
