# Generated by Django 3.2.6 on 2021-08-29 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_auto_20210828_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='fav',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
