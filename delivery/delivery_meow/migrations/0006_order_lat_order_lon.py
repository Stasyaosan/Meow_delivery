# Generated by Django 5.0.6 on 2024-05-30 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_meow', '0005_alter_order_courier'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='lat',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='lon',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
