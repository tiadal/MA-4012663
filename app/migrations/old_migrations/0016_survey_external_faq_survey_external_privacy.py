# Generated by Django 4.0.4 on 2022-06-29 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_variabletemplates_text_external_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='external_faq',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='external_privacy',
            field=models.TextField(blank=True, null=True),
        ),
    ]