# Generated by Django 3.2.6 on 2021-09-15 16:57

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_auto_20210911_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myprofile',
            name='member_id',
            field=models.PositiveIntegerField(blank=True, default=accounts.models.from_20300, editable=False, null=True, unique=True),
        ),
    ]