# Generated by Django 4.1.7 on 2023-05-04 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0002_rename_email_departments_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientservices',
            old_name='serviceCreatedData',
            new_name='serviceCreatedDate',
        ),
    ]