from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_title', models.CharField(default='GROCEFY', max_length=100, verbose_name='Site Title')),
                ('site_logo', models.ImageField(blank=True, null=True, upload_to='settings/', verbose_name='Site Logo')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='settings/', verbose_name='Favicon')),
                ('site_description', models.TextField(blank=True, verbose_name='Site Description')),
                ('site_keywords', models.TextField(blank=True, verbose_name='Site Keywords')),
                ('site_status', models.CharField(choices=[('active', 'Active'), ('maintenance', 'Maintenance')], default='active', max_length=20, verbose_name='Site Status')),
                ('maintenance_message', models.TextField(blank=True, verbose_name='Maintenance Message')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=50, verbose_name='Phone')),
                ('address', models.TextField(blank=True, verbose_name='Address')),
                ('facebook', models.URLField(blank=True, verbose_name='Facebook URL')),
                ('twitter', models.URLField(blank=True, verbose_name='Twitter URL')),
                ('instagram', models.URLField(blank=True, verbose_name='Instagram URL')),
                ('youtube', models.URLField(blank=True, verbose_name='YouTube URL')),
                ('linkedin', models.URLField(blank=True, verbose_name='LinkedIn URL')),
                ('currency', models.CharField(default='USD', max_length=10, verbose_name='Currency')),
                ('currency_symbol', models.CharField(default='$', max_length=5, verbose_name='Currency Symbol')),
                ('paypal_client_id', models.CharField(blank=True, max_length=255, verbose_name='PayPal Client ID')),
                ('paypal_secret', models.CharField(blank=True, max_length=255, verbose_name='PayPal Secret')),
                ('paypal_sandbox_mode', models.BooleanField(default=True, verbose_name='PayPal Sandbox Mode')),
                ('smtp_host', models.CharField(blank=True, max_length=100, verbose_name='SMTP Host')),
                ('smtp_port', models.CharField(blank=True, max_length=10, verbose_name='SMTP Port')),
                ('smtp_username', models.CharField(blank=True, max_length=100, verbose_name='SMTP Username')),
                ('smtp_password', models.CharField(blank=True, max_length=100, verbose_name='SMTP Password')),
                ('smtp_from_email', models.EmailField(blank=True, max_length=254, verbose_name='From Email')),
                ('footer_copyright', models.TextField(blank=True, default='© 2023 GROCEFY. All rights reserved.', verbose_name='Footer Copyright')),
                ('google_analytics', models.CharField(blank=True, max_length=50, verbose_name='Google Analytics ID')),
                ('default_tax_rate', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Default Tax Rate (%)')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
            ],
            options={
                'verbose_name': 'Settings',
                'verbose_name_plural': 'Settings',
            },
        ),
    ]