# Generated by Django 4.1.7 on 2023-03-30 10:07

from django.db import migrations, models
import subisu.models


class Migration(migrations.Migration):

    dependencies = [
        ('subisu', '0003_alter_activities_otheremails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activities',
            name='otherEmails',
            field=models.TextField(blank=True, help_text='Add other emails separated by spaces', null=True, validators=[subisu.models.validate_email_list]),
        ),
    ]
