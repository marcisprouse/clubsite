# Generated by Django 3.2.6 on 2021-09-01 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0028_alter_memberrsvp_bringing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberrsvp',
            name='bringing',
            field=models.TextField(blank=True, default='', help_text='If you are attending, please indicate what you may bring based on the request in the description of this event (i.e., dish, item for yard sale, etc.)', null=True),
        ),
    ]