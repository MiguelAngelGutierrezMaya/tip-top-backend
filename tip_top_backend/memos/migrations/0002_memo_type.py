# Generated by Django 2.2.12 on 2020-10-14 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='memo',
            name='type',
            field=models.CharField(choices=[('DRAFT', 'Draft Type'), ('PUBLIC', 'Public Type')], default='DRAFT', max_length=30),
        ),
    ]
