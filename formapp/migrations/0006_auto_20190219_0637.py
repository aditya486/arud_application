# Generated by Django 2.1.7 on 2019-02-19 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formapp', '0005_employee_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='Programming_Languages',
            field=models.CharField(choices=[('C', 'C++'), ('JAVA', 'Core JAVA'), ('Python', 'Advanced Python Django'), ('C#', 'C Sharp'), ('.net', 'ASP.net'), ('Mag', 'Magento2'), ('sft', 'Swift'), ('Web', 'HTML CSS'), ('net', 'networking')], max_length=10),
        ),
    ]
