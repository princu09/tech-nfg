# Generated by Django 3.0 on 2022-02-06 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('t_updates', '0012_auto_20220206_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='order_Items',
            field=models.TextField(),
        ),
    ]
