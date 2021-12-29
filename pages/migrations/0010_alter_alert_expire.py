# Generated by Django 3.2.6 on 2021-09-25 22:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_alter_alert_expire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='expire',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Put in the day/time you would like for this alert to expire (no longer show up on the site).'),
        ),
    ]