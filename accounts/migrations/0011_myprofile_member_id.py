# Generated by Django 3.2.6 on 2021-08-22 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_myprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='myprofile',
            name='member_id',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
    ]
