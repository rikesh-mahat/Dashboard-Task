# Generated by Django 4.1.7 on 2023-03-14 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0002_applicationaccess_applicationaccessmethod_and_more'),
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
        migrations.AlterField(
            model_name='applicationaccess',
            name='applicationAccessMethod',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='applicationaccess',
            name='applicationUserId',
            field=models.IntegerField(),
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
        migrations.AlterField(
            model_name='applicationaccess',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Models.staffs'),
        ),
        migrations.DeleteModel(
            name='Employees',
        ),
    ]
