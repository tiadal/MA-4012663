# Generated by Django 4.0.6 on 2023-01-02 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_remove_finalsurvey_contextual_matching_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='countersurvey',
            name='cm',
        ),
    ]