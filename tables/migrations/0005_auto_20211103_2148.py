# Generated by Django 3.2.6 on 2021-11-04 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0004_alter_table_theme_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='content_type',
            field=models.CharField(blank=True, help_text='The MIMEType of the file', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='table',
            name='picture',
            field=models.BinaryField(blank=True, editable=True, help_text='Add a picture of your table inspiration, if you like.', null=True),
        ),
    ]