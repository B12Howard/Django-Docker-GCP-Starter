# Generated by Django 3.1.5 on 2021-04-12 00:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0015_auto_20210411_2345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bizevent',
            name='client',
        ),
        migrations.AddField(
            model_name='bizevent',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_to_biz_event', to='App.companyprofile'),
        ),
    ]
