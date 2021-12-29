# Generated by Django 3.2.6 on 2021-08-21 03:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0006_alter_certificate_is_for_sale_as_of_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='is_for_sale_as_of_date',
            field=models.DateField(blank=True, default='', help_text='Enter date the certificate is for sale.  Delete default date of now if not for sale.', null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='purchase_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
