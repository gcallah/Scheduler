# Generated by Django 2.1.2 on 2019-05-02 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0027_request_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='date_time',
            field=models.CharField(default='', max_length=128, unique=True),
        ),
    ]
