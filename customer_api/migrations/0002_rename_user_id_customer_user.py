# Generated by Django 5.1.4 on 2024-12-13 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='user_id',
            new_name='user',
        ),
    ]