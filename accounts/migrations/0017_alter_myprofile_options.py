# Generated by Django 3.2.6 on 2021-08-23 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_myprofile_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myprofile',
            options={'managed': True, 'ordering': ['user']},
        ),
    ]
