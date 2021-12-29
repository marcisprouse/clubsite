# Generated by Django 3.2.6 on 2021-08-13 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minutes', '0008_alter_postminute_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postminute',
            name='slug',
            field=models.SlugField(help_text='This field automatically populates as you type the title.  Should look like this example: august-8-2021-board-meeting.', max_length=250, unique_for_date='publish'),
        ),
    ]