# Generated by Django 3.0 on 2022-02-07 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('t_updates', '0014_order_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]