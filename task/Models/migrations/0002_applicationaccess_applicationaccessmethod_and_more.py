# Generated by Django 4.1.7 on 2023-03-09 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationaccess',
            name='applicationAccessMethod',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='applicationaccess',
            name='applicationAccountStatus',
            field=models.BooleanField(default=True),
        ),
    ]
