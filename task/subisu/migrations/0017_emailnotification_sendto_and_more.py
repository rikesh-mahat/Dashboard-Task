# Generated by Django 4.1 on 2023-02-21 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subisu', '0016_remove_activities_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailnotification',
            name='sendTo',
            field=models.CharField(choices=[('Department', 'Department'), ('Client', 'Client')], default='Department', max_length=20),
        ),
        migrations.AlterField(
            model_name='emailnotification',
            name='sendStatus',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Open', 'Open'), ('Close', 'Close')], default='Open', max_length=25, verbose_name='Status'),
        ),
        migrations.CreateModel(
            name='Activity_Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, max_length=500, null=True)),
                ('commentBy', models.CharField(max_length=100)),
                ('actId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='subisu.activities')),
            ],
        ),
    ]
