# Generated by Django 3.2.6 on 2021-08-20 23:04

import address.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0004_auto_20210820_0950'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate_number', models.PositiveIntegerField(help_text='This number may not be greater than 2147483647', unique=True)),
                ('purchase_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('certificate_notes', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('member_coyote_lakes_address', address.models.AddressField(blank=True, help_text='Enter the Coyote Lakes address associated with the certificate number.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='member_coyote_lakes_address', to='address.address')),
            ],
        ),
    ]
