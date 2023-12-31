# Generated by Django 4.1.4 on 2023-08-13 18:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id_Admin', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id_Patient', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('cle', models.CharField(max_length=50)),
                ('date_naissance', models.DateField()),
                ('id_admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cliche',
            fields=[
                ('id_Cliche', models.AutoField(primary_key=True, serialize=False)),
                ('cle', models.CharField(max_length=50)),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Analyse',
            fields=[
                ('id_analyse', models.AutoField(primary_key=True, serialize=False)),
                ('fichier', models.FileField(upload_to='uploads/')),
                ('date', models.DateField()),
                ('admin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.patient')),
            ],
        ),
    ]
