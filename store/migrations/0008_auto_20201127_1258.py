# Generated by Django 3.1.3 on 2020-11-27 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20201122_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('S', 'Shirt'), ('SH', 'Shoe'), ('SW', 'Sport wear'), ('OW', 'Outwear')], max_length=2),
        ),
    ]
