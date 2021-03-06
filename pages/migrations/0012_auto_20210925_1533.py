# Generated by Django 3.2.6 on 2021-09-25 22:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0011_feature_expire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text="When do you want the alert to appear? If you are featuring more than one Alert on the homepage, the date that is closest to 'now' will appear first on the page."),
        ),
        migrations.AlterField(
            model_name='feature',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text="When do you want this flyer to appear on the site? If you are featuring more than one flyer on the homepage, the date that is closest to 'now' will appear first on the page."),
        ),
    ]
