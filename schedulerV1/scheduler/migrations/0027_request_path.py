# Generated by Django 2.1.2 on 2019-05-02 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0026_auto_20190501_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='path',
            field=models.CharField(default='', max_length=128),
        ),
    ]
