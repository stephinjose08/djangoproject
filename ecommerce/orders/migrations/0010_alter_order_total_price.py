# Generated by Django 3.2.14 on 2022-08-09 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_canceled_orders_cancel_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.FloatField(),
        ),
    ]
