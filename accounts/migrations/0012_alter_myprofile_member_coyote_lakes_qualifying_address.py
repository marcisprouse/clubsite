# Generated by Django 3.2.6 on 2021-08-22 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0015_alter_certificate_member_coyote_lakes_address'),
        ('accounts', '0011_myprofile_member_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myprofile',
            name='member_coyote_lakes_qualifying_address',
            field=models.ForeignKey(blank=True, help_text='Choose address from dropdown, if applies to this profile.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='member_coyote_lakes_qualifying_address', to='certificates.certificate'),
        ),
    ]
