# Generated by Django 4.1.7 on 2023-03-09 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField(max_length=500)),
                ('devLanguage', models.CharField(max_length=200)),
                ('sourceCode', models.CharField(max_length=200)),
                ('serverAccess', models.CharField(max_length=50)),
                ('serverControl', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empName', models.CharField(max_length=200)),
                ('mobile', models.BigIntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('cugNumber', models.BigIntegerField()),
                ('branch', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=200)),
                ('unit', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('working', models.CharField(max_length=50)),
                ('empGroup', models.CharField(max_length=200)),
                ('supervisor1', models.CharField(max_length=150)),
                ('supervisor2', models.CharField(max_length=150)),
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
            name='ApplicationAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicationId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_id', to='Models.applications')),
                ('applicationUserId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='application_id', to='Models.employees')),
                ('previligeId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Models.priviliges')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Models.employees')),
            ],
        ),
    ]