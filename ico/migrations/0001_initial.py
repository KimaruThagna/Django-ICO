# Generated by Django 3.1.7 on 2021-08-30 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TreasuryConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_window', models.IntegerField(default=3)),
                ('token_max_price', models.IntegerField(default=100)),
                ('treasury_supply', models.IntegerField(default=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('token_balance', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_tokens', models.IntegerField()),
                ('bidding_price', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('successful', models.BooleanField(default=False)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ico.users')),
            ],
        ),
    ]
