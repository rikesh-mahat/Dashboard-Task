# Generated by Django 4.1.7 on 2023-05-09 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subisu', '0009_alter_activities_eta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activities',
            name='endTime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Activity End Time'),
        ),
        migrations.AlterField(
            model_name='activities',
            name='startTime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Activity Start Time'),
        ),
    ]
