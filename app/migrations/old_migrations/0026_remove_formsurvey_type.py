# Generated by Django 4.0.4 on 2022-06-30 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_survey_form_start_survey_forms_survey_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formsurvey',
            name='type',
        ),
    ]
