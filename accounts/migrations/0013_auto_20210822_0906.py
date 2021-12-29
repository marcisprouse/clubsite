# Generated by Django 3.2.6 on 2021-08-22 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_myprofile_member_coyote_lakes_qualifying_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='myprofile',
            name='birthdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='myprofile',
            name='about_me',
            field=models.TextField(blank=True, verbose_name='about me'),
        ),
        migrations.AlterField(
            model_name='myprofile',
            name='favorite_activity',
            field=models.CharField(blank=True, max_length=125, verbose_name='favorite activity'),
        ),
        migrations.AlterField(
            model_name='myprofile',
            name='favorite_snack',
            field=models.CharField(blank=True, max_length=125, verbose_name='favorite snack'),
        ),
        migrations.AlterField(
            model_name='myprofile',
            name='member_notes',
            field=models.TextField(blank=True, help_text='For administrative purposes', verbose_name='member notes'),
        ),
    ]