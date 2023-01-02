# Generated by Django 4.0.4 on 2022-06-26 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_remove_surveyuser_survey_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_id', models.IntegerField(default=0)),
                ('case_settings', models.JSONField(default=dict)),
                ('case_answer', models.JSONField(default=dict)),
                ('survey_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.survey')),
                ('survey_user_ud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.surveyuser')),
            ],
        ),
    ]
