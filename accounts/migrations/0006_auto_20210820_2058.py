# Generated by Django 3.2.6 on 2021-08-21 03:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210820_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myprofile',
            name='date_entered',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='myprofile',
            name='date_first_entered',
            field=models.DateField(blank=True, default=django.utils.timezone.now, help_text='Enter date first entered from old table information.'),
        ),
    ]