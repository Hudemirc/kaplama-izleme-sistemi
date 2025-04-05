# Generated by Django 4.2.20 on 2025-04-05 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_pallet_length_group_alter_pallet_shipment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pallet',
            name='currency',
            field=models.CharField(choices=[('TRY', '₺ Türk Lirası'), ('USD', '$ Amerikan Doları'), ('EUR', '€ Euro')], default='TRY', max_length=3, verbose_name='Para Birimi'),
        ),
        migrations.AlterField(
            model_name='pallet',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Birim Fiyat'),
        ),
    ]
