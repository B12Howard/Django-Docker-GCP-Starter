# Generated by Django 3.1.5 on 2021-04-02 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_auto_20210402_0118'),
    ]

    operations = [
        migrations.AddField(
            model_name='bizevent',
            name='drive_folder_id',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
