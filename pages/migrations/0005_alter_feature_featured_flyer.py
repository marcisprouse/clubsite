# Generated by Django 3.2.6 on 2021-09-25 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20210925_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='featured_flyer',
            field=models.FileField(blank=True, help_text='Convert your .doc Flyer File to a .jpg. There are online tools to do this.  One of them is https://cloudconvert.com/docx-to-jpg', null=True, upload_to='pages/images/feature'),
        ),
    ]