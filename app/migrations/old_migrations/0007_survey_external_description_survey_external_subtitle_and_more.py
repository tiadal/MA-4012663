# Generated by Django 4.0.4 on 2022-06-25 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_surveyuser_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='external_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='external_subtitle',
            field=models.CharField(blank=True, max_length=320, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='external_title',
            field=models.CharField(default='Survey', max_length=160),
        ),
    ]