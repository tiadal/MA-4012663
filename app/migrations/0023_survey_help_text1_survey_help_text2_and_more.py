# Generated by Django 4.0.6 on 2022-08-30 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_finalusers_academic_finalusers_context_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='help_text1',
            field=models.CharField(blank=True, max_length=320, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='help_text2',
            field=models.CharField(blank=True, max_length=320, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='help_title',
            field=models.CharField(blank=True, max_length=320, null=True),
        ),
    ]