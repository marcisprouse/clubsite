# Generated by Django 3.2.6 on 2021-11-04 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0003_auto_20211103_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='theme_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
