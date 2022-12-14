# Generated by Django 3.2.14 on 2022-08-10 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_alter_canceled_orders_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('out  for  shipping', 'out or shipping'), ('completed', 'completed'), ('canceled', 'canceled'), ('returned', 'returned')], default='pending', max_length=50),
        ),
    ]
