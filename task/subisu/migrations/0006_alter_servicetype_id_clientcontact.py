# Generated by Django 4.1.7 on 2023-02-16 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subisu', '0005_servicetype_service_srvtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicetype',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.CreateModel(
            name='ClientContact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('mobile', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=150)),
                ('status', models.BooleanField(default=False)),
                ('registerDate', models.DateTimeField(auto_now_add=True)),
                ('srvid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='subisu.service')),
            ],
        ),
    ]
