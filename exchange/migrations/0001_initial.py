# Generated by Django 3.1.1 on 2020-09-28 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('analyzer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid', models.BooleanField(default=False)),
                ('mini', models.BooleanField(default=False)),
                ('deposit_share', models.DecimalField(decimal_places=0, default=0, max_digits=2)),
                ('entry_zone_low', models.DecimalField(decimal_places=8, max_digits=16)),
                ('entry_zone_high', models.DecimalField(decimal_places=8, max_digits=16)),
                ('targets', models.CharField(max_length=511)),
                ('stop_loss', models.DecimalField(decimal_places=8, max_digits=16)),
                ('cross_leverage', models.BooleanField(default=False)),
                ('leverage', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('trajectory', models.TextField(blank=True, null=True)),
                ('last_price', models.DecimalField(decimal_places=8, default=0, max_digits=16)),
                ('last_price_sell', models.DecimalField(decimal_places=8, default=0, max_digits=16)),
                ('bot_message_id', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('should_have_socket', models.BooleanField(default=True)),
                ('creator_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='analyzer.profile')),
            ],
        ),
        migrations.CreateModel(
            name='SignalResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profit', models.CharField(max_length=255)),
                ('first_target_profit', models.CharField(max_length=255)),
                ('has_won', models.BooleanField()),
                ('signal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exchange.signal')),
            ],
        ),
    ]
