# Generated by Django 3.2.6 on 2021-09-25 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0044_alter_myprofile_temporary_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myprofile',
            name='temporary_password',
            field=models.CharField(default='pa$$word', help_text="Enter the temporary password you provided to create this user's account. Be EXACT since they will use this password to log in for the first time.", max_length=25),
        ),
    ]
