# Generated by Django 3.1.5 on 2021-04-10 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0013_auto_20210410_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='company_website',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='client',
            name='contact_person',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='client',
            name='contact_person_email',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='client',
            name='contact_person_phone',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='client',
            name='contact_person_position',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='client',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
