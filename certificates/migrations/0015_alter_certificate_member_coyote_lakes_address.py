# Generated by Django 3.2.6 on 2021-08-22 03:02

import address.models
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0004_auto_20210820_0950'),
        ('certificates', '0014_alter_certificate_purchase_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='member_coyote_lakes_address',
            field=address.models.AddressField(blank=True, help_text='Enter the Coyote Lakes address associated with the certificate number.  If the address does not exist in the dropdown, it needs to be added in the Certificate table.  If the certificate does not have an address associated with it, use the club address.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='member_coyote_lakes_address', to='address.address'),
        ),
    ]
