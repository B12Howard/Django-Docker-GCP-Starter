# Generated by Django 3.1.5 on 2021-04-02 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0006_auto_20210401_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendortobizevent',
            name='analyst_assigned_vendor',
            field=models.BooleanField(default=False, help_text='True means the vendor can sign the nda, False means cannot proceed'),
        ),
    ]
