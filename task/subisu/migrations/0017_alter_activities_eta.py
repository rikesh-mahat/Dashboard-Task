# Generated by Django 4.2.1 on 2023-06-22 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subisu', '0016_activities_empid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activities',
            name='ETA',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
