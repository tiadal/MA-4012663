# Generated by Django 4.0.6 on 2022-08-25 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_countersurvey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countersurvey',
            name='cm',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='countersurvey',
            name='co',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='countersurvey',
            name='se',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='countersurvey',
            name='tr',
            field=models.BooleanField(),
        ),
    ]
