# Generated by Django 2.1.3 on 2018-12-02 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0014_course_pname'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Professor',
        ),
    ]