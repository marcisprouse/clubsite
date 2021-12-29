# Generated by Django 3.2.6 on 2021-08-21 17:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0013_alter_certificate_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='purchase_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, help_text='Delete date if not purchased yet.', null=True),
        ),
    ]
