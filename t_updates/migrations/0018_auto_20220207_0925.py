# Generated by Django 3.0 on 2022-02-07 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('t_updates', '0017_order_item_length'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='item_Length',
            new_name='itemLen',
        ),
    ]
