# Generated by Django 2.1.7 on 2019-02-28 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formapp', '0016_employee_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='Image',
            field=models.ImageField(default='media/default.jpg', upload_to='profile_pics'),
        ),
    ]
