# Generated by Django 3.1.3 on 2020-11-27 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20201127_1258'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_date',
            new_name='ordered_date',
        ),
    ]
