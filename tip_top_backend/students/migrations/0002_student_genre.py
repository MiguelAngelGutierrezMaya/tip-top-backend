# Generated by Django 2.2.12 on 2020-09-29 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='genre',
            field=models.CharField(choices=[('MALE', 'Male Type'), ('FEMALE', 'Female Type')], default='MALE', max_length=30),
        ),
    ]
