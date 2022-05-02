# Generated by Django 3.1.5 on 2021-04-12 19:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App', '0019_usertoclient'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyToUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_user', to='App.companyprofile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_company', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
