# Generated by Django 3.2.6 on 2021-08-30 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0018_auto_20210830_1418'),
    ]

    operations = [
        migrations.RenameField(
            model_name='occurrence',
            old_name='volunteers',
            new_name='need_volunteers',
        ),
    ]