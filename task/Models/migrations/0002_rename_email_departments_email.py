# Generated by Django 4.1.7 on 2023-04-30 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='departments',
            old_name='email',
            new_name='Email',
        ),
    ]
