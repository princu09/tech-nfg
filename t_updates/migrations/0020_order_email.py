# Generated by Django 3.0 on 2022-02-13 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('t_updates', '0019_order_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default='pri2232@outlook.com', max_length=254),
            preserve_default=False,
        ),
    ]