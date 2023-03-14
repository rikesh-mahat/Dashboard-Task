# Generated by Django 4.1.7 on 2023-02-16 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subisu', '0002_host_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('serviceName', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='service',
            name='hostName',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='srvType',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='subisu.servicetype'),
        ),
    ]