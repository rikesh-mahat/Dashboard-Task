# Generated by Django 4.1 on 2023-02-21 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subisu', '0017_emailnotification_sendto_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailnotification',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
