# Generated by Django 5.1.4 on 2024-12-13 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provider_api', '0005_order_delivery_fee_order_provider_fee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='delivery',
            new_name='deliver',
        ),
    ]