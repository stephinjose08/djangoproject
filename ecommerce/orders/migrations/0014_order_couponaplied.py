# Generated by Django 3.2.14 on 2022-08-15 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_returned_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='couponaplied',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
