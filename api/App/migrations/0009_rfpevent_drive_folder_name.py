# Generated by Django 3.1.5 on 2021-04-03 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_bizevent_drive_folder_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='bizevent',
            name='drive_folder_name',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
