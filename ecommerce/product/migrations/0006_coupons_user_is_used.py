# Generated by Django 3.2.14 on 2022-08-06 17:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0005_coupons_discount_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupons',
            name='user_is_used',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
