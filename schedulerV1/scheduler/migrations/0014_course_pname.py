# Generated by Django 2.1.3 on 2018-12-02 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0013_auto_20181202_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='pname',
            field=models.CharField(default='', max_length=128),
        ),
    ]
