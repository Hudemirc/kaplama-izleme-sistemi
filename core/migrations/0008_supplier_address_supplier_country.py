# Generated by Django 4.2.20 on 2025-04-05 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_supplier_email_alter_supplier_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='address',
            field=models.TextField(blank=True, verbose_name='Adres'),
        ),
        migrations.AddField(
            model_name='supplier',
            name='country',
            field=models.CharField(blank=True, max_length=100, verbose_name='Ülke'),
        ),
    ]
