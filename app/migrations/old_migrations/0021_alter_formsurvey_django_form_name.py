# Generated by Django 4.0.4 on 2022-06-30 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_rename_form_text_formsurvey_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formsurvey',
            name='django_form_name',
            field=models.CharField(choices=[('Radio5', 'Radio5'), ('Radio7', 'Radio7'), ('Text1', 'Text1')], default='Text1', max_length=32),
        ),
    ]
