# Generated by Django 3.2.6 on 2021-08-27 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_auto_20210827_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myprofile',
            name='favorite_activity',
            field=models.TextField(blank=True, verbose_name='favorite activity'),
        ),
        migrations.AlterField(
            model_name='myprofile',
            name='favorite_snack',
            field=models.CharField(blank=True, help_text='    ', max_length=125, verbose_name='favorite snack'),
        ),
    ]
