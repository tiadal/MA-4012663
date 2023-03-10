# Generated by Django 4.0.6 on 2022-08-23 12:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FormSurvey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Form', max_length=32)),
                ('language', models.CharField(choices=[('DE', 'German'), ('EN', 'English'), ('IT', 'Italian'), ('ES', 'Spanish')], default='EN', max_length=2)),
                ('text', models.TextField(blank=True, default='Please fill the form', null=True)),
                ('django_form_name', models.CharField(choices=[('Radio5', 'Radio5'), ('Radio7', 'Radio7'), ('Text1', 'Text1'), ('NewSurveyUser', 'NewSurveyUser'), ('NewSurveyUserIT', 'NewSurveyUserIT'), ('Radio50', 'Radio50')], default='Text1', max_length=32)),
                ('template_tag', models.CharField(blank=True, default='', max_length=32)),
                ('is_start', models.BooleanField(blank=True, default=False)),
                ('text_button', models.TextField(blank=True, default='Save', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160)),
                ('language', models.CharField(choices=[('DE', 'German'), ('EN', 'English'), ('IT', 'Italian'), ('ES', 'Spanish')], default='EN', max_length=2)),
                ('description', models.CharField(blank=True, max_length=320, null=True)),
                ('survey_zero', models.BooleanField(default=False)),
                ('external_title', models.CharField(default='Survey', max_length=160)),
                ('external_subtitle', models.CharField(blank=True, max_length=320, null=True)),
                ('external_description', models.TextField(blank=True, null=True)),
                ('external_faq', models.TextField(blank=True, null=True)),
                ('external_privacy', models.TextField(blank=True, null=True)),
                ('variables', models.JSONField(default=dict)),
                ('title_case', models.CharField(default='Case', max_length=160)),
                ('title_question', models.CharField(default='Questions', max_length=160)),
                ('first_survey', models.BooleanField(default=False)),
                ('last_survey', models.BooleanField(default=False)),
                ('survey_end_text', models.CharField(default='Thanks.', max_length=720)),
                ('form_start', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='form_start', to='app.formsurvey')),
                ('form_survey', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='form_survey', to='app.formsurvey')),
                ('survey_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.survey')),
                ('user_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_settings', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='VariablesCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=2)),
                ('name', models.CharField(max_length=32)),
                ('description', models.CharField(blank=True, max_length=320, null=True)),
                ('max_segments', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='VariableTemplates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='Template', max_length=32, null=True)),
                ('settings', models.JSONField(default=dict)),
                ('segment', models.JSONField(default=dict)),
                ('text_internal', models.CharField(blank=True, default=None, max_length=3200, null=True)),
                ('text_external', models.CharField(blank=True, default=None, max_length=3200, null=True)),
                ('code_html', models.TextField(blank=True, default=None, null=True)),
                ('code_css', models.TextField(blank=True, default=None, null=True)),
                ('code_js', models.TextField(blank=True, default=None, null=True)),
                ('zero_template', models.BooleanField(default=False)),
                ('variable_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.variablescategory')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_id', models.IntegerField(default=0)),
                ('case_settings', models.JSONField(default=dict)),
                ('case_answer', models.JSONField(default=dict)),
                ('survey_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.survey')),
                ('survey_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.surveyuser')),
            ],
        ),
        migrations.CreateModel(
            name='Partners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160)),
                ('partner_type', models.CharField(choices=[('Company', 'company'), ('Agency', 'agency'), ('Creator', 'creator')], default='company', max_length=8)),
                ('description', models.CharField(blank=True, max_length=320, null=True)),
                ('hubspot_company', models.CharField(blank=True, max_length=320, null=True)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
