# Generated by Django 3.2.14 on 2022-08-06 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_canceled_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='canceled_orders',
            name='reason_for_cancel',
            field=models.TextField(blank=True, choices=[('order  placed by mistake', 'order  placed by mistake'), ('price for the product has decreased', 'price for the product has decreased'), ('i have purchased the product elsewhere', 'i have purchased the product elsewhere'), ('i want to cance  due to the prodduct quality issues', 'i want to cance  due to the prodduct quality issues')], null=True),
        ),
    ]
