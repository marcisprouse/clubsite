# Generated by Django 3.2.6 on 2021-09-25 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0012_auto_20210925_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', help_text='If set to Draft, the alert will NEVER appear. If set to Published, the alert will appear between the set Publish and Expire dates.', max_length=10),
        ),
        migrations.AlterField(
            model_name='feature',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', help_text='If set to Draft, the feature FLYER will NEVER appear. If set to Published, the feature FLYER will appear between the set Publish and Expire dates.', max_length=10),
        ),
    ]
