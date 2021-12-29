# Generated by Django 3.2.6 on 2021-09-18 23:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=250, unique_for_date='publish')),
                ('feature_title', models.CharField(blank=True, default=None, max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
                ('feature_day_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('feature_location', models.CharField(blank=True, default=None, max_length=250)),
                ('featured_flyer', models.FileField(blank=True, null=True, upload_to='pages/images/feature')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
    ]