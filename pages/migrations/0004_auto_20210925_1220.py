# Generated by Django 3.2.6 on 2021-09-25 19:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_alter_feature_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='feature_day_time',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='This is the date/time of the actual activity...not the day you want it published'),
        ),
        migrations.AlterField(
            model_name='feature',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text="Use now, or 'today'. If you are featuring more than one flyer on the homepage, the date that is closest to 'now' will appear first on the page."),
        ),
    ]
