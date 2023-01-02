# Generated by Django 4.0.6 on 2022-08-26 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_countersurvey_unique_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinalUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(blank=True, default=0, null=True)),
                ('lang_de', models.BooleanField(blank=True, default=False, null=True)),
                ('lang_it', models.BooleanField(blank=True, default=False, null=True)),
                ('lang_en', models.BooleanField(blank=True, default=False, null=True)),
                ('lang_es', models.BooleanField(blank=True, default=False, null=True)),
                ('lang_ot', models.BooleanField(blank=True, default=False, null=True)),
                ('gend_m', models.BooleanField(blank=True, default=False, null=True)),
                ('gend_f', models.BooleanField(blank=True, default=False, null=True)),
                ('gend_x', models.BooleanField(blank=True, default=False, null=True)),
                ('age', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
    ]
