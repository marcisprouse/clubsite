# Generated by Django 3.2.6 on 2021-09-19 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0037_remove_myprofile_birthdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='myprofile',
            name='birthdate',
            field=models.DateField(blank=True, help_text="Format: YYYY-MM-DD. We don't disclose the year. Enter if you'd like to be on our birthday lists.", null=True),
        ),
    ]
