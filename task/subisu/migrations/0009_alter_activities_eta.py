# Generated by Django 4.1.7 on 2023-05-09 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subisu', '0008_remove_activities_maintenancewindow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activities',
            name='ETA',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]