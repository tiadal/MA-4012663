# Generated by Django 4.0.6 on 2022-08-28 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_finalsurvey'),
    ]

    operations = [
        migrations.RenameField(
            model_name='finalusers',
            old_name='age',
            new_name='age_range',
        ),
    ]
