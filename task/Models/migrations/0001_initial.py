# Generated by Django 4.1.7 on 2023-03-14 12:01

import Models.client_services
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('status', models.BooleanField(default=True)),
                ('vpName', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Hosts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deviceId', models.IntegerField()),
                ('hostname', models.CharField(max_length=200)),
                ('deviceType', models.CharField(max_length=200)),
                ('popName', models.CharField(max_length=250)),
                ('popLatitude', models.BigIntegerField()),
                ('pioLatitude', models.BigIntegerField()),
                ('modelName', models.CharField(max_length=250)),
                ('districtname', models.CharField(max_length=250)),
                ('regionName', models.CharField(max_length=250)),
                ('provinceName', models.CharField(max_length=250)),
                ('branchName', models.CharField(max_length=250)),
                ('hyperVisor', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Priviliges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preLevel', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('srvType', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Units',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('unitHead', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('status', models.BooleanField(default=True)),
                ('departmentId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Models.departments')),
            ],
        ),
        migrations.CreateModel(
            name='Staffs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=100)),
                ('middleName', models.CharField(blank=True, max_length=100, null=True)),
                ('lastName', models.CharField(max_length=100)),
                ('empId', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('status', models.BooleanField(default=True)),
                ('unitId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Models.units')),
            ],
        ),
        migrations.CreateModel(
            name='ClientServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domainName', models.CharField(max_length=250)),
                ('primaryContactName', models.CharField(max_length=250)),
                ('primaryContactNumber', models.BigIntegerField(validators=[Models.client_services.mobile_number_validation])),
                ('primaryContactEmail', models.EmailField(max_length=254)),
                ('secondaryContactName', models.CharField(max_length=250)),
                ('secondaryContactNumber', models.BigIntegerField(validators=[Models.client_services.mobile_number_validation])),
                ('secondaryContactEmail', models.EmailField(max_length=254)),
                ('serviceStatus', models.BooleanField(default=True)),
                ('serviceCreatedData', models.DateTimeField()),
                ('hostId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Models.hosts')),
                ('srvType', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Models.servicetypes')),
            ],
        ),
        migrations.CreateModel(
            name='Applications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField(max_length=500)),
                ('devLanguage', models.CharField(max_length=200)),
                ('sourceCode', models.CharField(choices=[('OPEN', 'OPEN'), ('CLOSE', 'CLOSE'), ('IN HOUSE', 'IN HOUSE')], max_length=200)),
                ('serverAccess', models.CharField(max_length=50)),
                ('serverControl', models.CharField(choices=[('Subisu', 'Subisu'), ('Vendor', 'Vendor'), ('Both', 'Both')], max_length=150)),
                ('hostId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Models.hosts')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicationUserId', models.IntegerField()),
                ('applicationAccountStatus', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Suspended', 'Suspended')], max_length=200)),
                ('applicationAccessMethod', models.CharField(choices=[('Web', 'Web'), ('Mobile App', 'Mobile App'), ('CLI', 'CLI')], max_length=100)),
                ('applicationId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_id', to='Models.applications')),
                ('previligeId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Models.priviliges')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Models.staffs')),
            ],
        ),
    ]
