# Generated by Django 4.2.1 on 2023-06-15 23:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subisu', '0014_alter_activitytable_comment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activities',
            name='benefits',
        ),
    ]
