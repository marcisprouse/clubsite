# Generated by Django 3.2.6 on 2021-08-23 01:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0018_alter_myprofile_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myprofile',
            name='user',
            field=models.OneToOneField(help_text='Process:  Add User through the https://www.coyotelakesrecreationclub.org/accounts/signup form, then follow steps in instructions.  If the user name is not in the drop down, you must add them to the User table first.  See instructions', on_delete=django.db.models.deletion.CASCADE, related_name='my_profile', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
