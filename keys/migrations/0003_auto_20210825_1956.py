# Generated by Django 3.2.6 on 2021-08-26 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0018_alter_certificate_name_associated_with_certificate'),
        ('keys', '0002_alter_key_member_coyote_lakes_qualifying_address_for_keys'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='key',
            options={'ordering': ['key_number_one']},
        ),
        migrations.AlterField(
            model_name='key',
            name='member_coyote_lakes_qualifying_address_for_keys',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='member_coyote_lakes_qualifying_address_for_keys', to='certificates.certificate', unique=True),
        ),
    ]
