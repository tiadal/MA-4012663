# Generated by Django 4.0.4 on 2022-06-30 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_alter_formsurvey_django_form_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyuser',
            name='user_settings',
            field=models.JSONField(default=dict),
        ),
    ]
