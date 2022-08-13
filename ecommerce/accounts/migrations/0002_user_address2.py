# Generated by Django 3.2.14 on 2022-08-09 11:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_address2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fist_name', models.CharField(default='null', max_length=100)),
                ('last_name', models.CharField(default='null', max_length=100)),
                ('email', models.CharField(default='null', max_length=100)),
                ('phone', models.CharField(default='null', max_length=15)),
                ('addressline1', models.CharField(default='null', max_length=200)),
                ('addressline2', models.CharField(default='null', max_length=200)),
                ('city', models.CharField(default='null', max_length=100)),
                ('state', models.CharField(default='null', max_length=100)),
                ('country', models.CharField(default='null', max_length=100)),
                ('zip_code', models.CharField(default='null', max_length=8)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
