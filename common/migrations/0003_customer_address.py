# Generated by Django 4.1.4 on 2023-03-01 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.CharField(default='', max_length=100),
        ),
    ]
