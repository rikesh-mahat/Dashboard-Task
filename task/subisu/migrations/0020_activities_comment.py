# Generated by Django 4.1.7 on 2023-02-21 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subisu', '0019_rename_activity_table_activitytable_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activities',
            name='comment',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
