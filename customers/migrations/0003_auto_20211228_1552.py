# Generated by Django 3.2.9 on 2021-12-28 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_auto_20211218_1712'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraddress',
            old_name='address_1',
            new_name='address_line_1',
        ),
        migrations.RenameField(
            model_name='useraddress',
            old_name='address_2',
            new_name='address_line_2',
        ),
        migrations.RenameField(
            model_name='useraddress',
            old_name='town',
            new_name='city',
        ),
    ]