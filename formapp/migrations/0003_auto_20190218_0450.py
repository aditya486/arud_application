# Generated by Django 2.1.7 on 2019-02-18 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formapp', '0002_auto_20190218_0442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='Mobile_No',
            field=models.CharField(max_length=11),
        ),
    ]
