# Generated by Django 3.2.6 on 2021-08-21 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210820_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myprofile',
            name='about_me',
            field=models.TextField(blank=True, verbose_name='about_me'),
        ),
    ]
