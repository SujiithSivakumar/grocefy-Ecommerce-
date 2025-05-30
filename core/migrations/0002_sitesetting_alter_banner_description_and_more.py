# Generated by Django 5.0.3 on 2025-04-20 09:21

import ckeditor.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_title', models.CharField(default='GROCEFY', max_length=100)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='photos/site/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='photos/site/', validators=[django.core.validators.FileExtensionValidator(['ico', 'png'])])),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('facebook_url', models.URLField(blank=True, null=True)),
                ('twitter_url', models.URLField(blank=True, null=True)),
                ('instagram_url', models.URLField(blank=True, null=True)),
                ('youtube_url', models.URLField(blank=True, null=True)),
                ('copyright_text', models.CharField(blank=True, max_length=255, null=True)),
                ('about_us', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('privacy_policy', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('terms_conditions', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Site Setting',
                'verbose_name_plural': 'Site Settings',
            },
        ),
        migrations.AlterField(
            model_name='banner',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='banner',
            name='photo',
            field=models.ImageField(upload_to='photos/banners/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])]),
        ),
        migrations.AlterField(
            model_name='banner',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=10),
        ),
    ]
