# Generated by Django 3.2.6 on 2021-08-13 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minutes', '0002_rename_postminutes_postminute'),
    ]

    operations = [
        migrations.AddField(
            model_name='postminute',
            name='attendance',
            field=models.TextField(blank=True, help_text='List attendees only, separated by commas.'),
        ),
    ]
