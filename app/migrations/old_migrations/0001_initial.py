# Generated by Django 4.0.4 on 2022-06-25 12:36

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
