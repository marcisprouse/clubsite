# Generated by Django 3.2.6 on 2021-10-24 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0046_alter_myprofile_temporary_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='myprofile',
            name='exclude_member_coyote_lakes_address_from_site',
            field=models.BooleanField(default=False, help_text='Check if member requests that their address does NOT show up on site information. Leave blank to keep address appearing on site.'),
        ),
    ]