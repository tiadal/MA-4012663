# Generated by Django 4.0.6 on 2022-08-26 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_finalsurveyzero'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinalSurvey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(blank=True, default=0, null=True)),
                ('case_id', models.IntegerField(blank=True, default=0, null=True)),
                ('sensitivity', models.IntegerField(blank=True, default=0, null=True)),
                ('context', models.IntegerField(blank=True, default=0, null=True)),
                ('transparency', models.IntegerField(blank=True, default=0, null=True)),
                ('contextual_matching', models.IntegerField(blank=True, default=0, null=True)),
                ('template_sensitivity', models.IntegerField(blank=True, default=0, null=True)),
                ('template_context', models.IntegerField(blank=True, default=0, null=True)),
                ('template_transparency', models.IntegerField(blank=True, default=0, null=True)),
                ('template_contextual_matching', models.IntegerField(blank=True, default=0, null=True)),
                ('answer_1', models.IntegerField(blank=True, default=0, null=True)),
                ('answer_2', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
    ]
