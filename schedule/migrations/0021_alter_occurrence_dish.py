# Generated by Django 3.2.6 on 2021-08-30 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0020_auto_20210830_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='dish',
            field=models.BooleanField(default=False, help_text='Check if you would like for members to sign up to bring a dish or item.  Be sure to have the details of dish ideas in your description.', verbose_name='member brings dish or item'),
        ),
    ]
