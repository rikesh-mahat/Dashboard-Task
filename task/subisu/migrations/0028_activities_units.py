# Generated by Django 4.1 on 2023-03-24 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0001_initial'),
        ('subisu', '0027_rename_message_emailnotification_emailbody_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activities',
            name='units',
            field=models.ManyToManyField(blank=True, null=True, to='Models.units'),
        ),
    ]
