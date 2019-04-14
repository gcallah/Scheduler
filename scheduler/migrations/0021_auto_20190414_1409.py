# Generated by Django 2.1.2 on 2019-04-14 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0020_day_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='time',
            name='days',
        ),
        migrations.AddField(
            model_name='time',
            name='times',
            field=models.CharField(choices=[('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22')], default='8', max_length=2),
            preserve_default=False,
        ),
    ]
