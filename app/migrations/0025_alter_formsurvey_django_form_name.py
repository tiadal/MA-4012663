# Generated by Django 4.0.6 on 2022-09-02 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_alter_formsurvey_django_form_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formsurvey',
            name='django_form_name',
            field=models.CharField(choices=[('Radio5', 'Radio5'), ('Radio5ITCON', 'Radio5ITCON'), ('Radio7', 'Radio7'), ('Text1', 'Text1'), ('NewSurveyUserEN', 'NewSurveyUserEN'), ('NewSurveyUserIT', 'NewSurveyUserIT'), ('Radio50', 'Radio50'), ('EmptyForm', 'EmptyForm')], default='Text1', max_length=32),
        ),
    ]
