# Generated by Django 3.2.6 on 2021-08-21 04:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0009_alter_certificate_purchase_date'),
        ('accounts', '0007_auto_20210820_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myprofile',
            name='member_coyote_lakes_qualifying_address',
            field=models.ForeignKey(blank=True, help_text='Choose address from dropdown.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member_coyote_lakes_qualifying_address', to='certificates.certificate'),
        ),
    ]
