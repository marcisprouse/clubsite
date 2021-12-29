# Generated by Django 3.2.6 on 2021-08-13 20:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('minutes', '0007_alter_postminute_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postminute',
            name='author',
            field=models.ForeignKey(help_text='Click on the magnifying glass and choose from that list.', on_delete=django.db.models.deletion.CASCADE, related_name='minutes_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]