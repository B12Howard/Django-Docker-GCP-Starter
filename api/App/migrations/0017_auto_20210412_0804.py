# Generated by Django 3.1.5 on 2021-04-12 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0016_auto_20210412_0057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='contact_person_position',
        ),
        migrations.AlterField(
            model_name='client',
            name='description',
            field=models.TextField(default='', null=True),
        ),
    ]
