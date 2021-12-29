# Generated by Django 3.2.6 on 2021-08-23 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_alter_myprofile_user'),
        ('certificates', '0015_alter_certificate_member_coyote_lakes_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='name_associated_with_certificate',
        ),
        migrations.AddField(
            model_name='certificate',
            name='main_name_associated_with_certificate',
            field=models.ForeignKey(blank=True, help_text='Choose one. If the main name/owner associated is not in the dropbox, you have to add the user account. See instructions.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='main_name_associated_with_certificate', to='accounts.myprofile'),
        ),
    ]