# Generated by Django 3.2.6 on 2021-08-21 04:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0008_alter_certificate_purchase_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='purchase_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, help_text='Delete date if not purchased yet.'),
        ),
    ]
