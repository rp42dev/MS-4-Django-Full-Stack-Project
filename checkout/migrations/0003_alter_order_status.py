# Generated by Django 3.2.9 on 2021-12-10 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending Payment', 'Pp'), ('Pending Shipment', 'Ps'), ('Shipped', 'Sh'), ('Canceled', 'Ca')], default='Pending Payment', max_length=100),
        ),
    ]