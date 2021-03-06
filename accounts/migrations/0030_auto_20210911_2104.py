# Generated by Django 3.2.6 on 2021-09-12 04:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_auto_20210911_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myprofile',
            name='cell_phone',
            field=models.CharField(blank=True, help_text='    ', max_length=16, null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')]),
        ),
        migrations.AlterField(
            model_name='myprofile',
            name='other_phone',
            field=models.CharField(blank=True, help_text='    ', max_length=16, null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')]),
        ),
    ]
