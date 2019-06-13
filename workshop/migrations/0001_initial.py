# Generated by Django 2.1 on 2018-09-18 18:56

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.TextField(max_length=500)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=2)),
                ('zip', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=100)),
                ('user', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('user', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2018, 9, 18, 14, 56, 12, 20295), verbose_name='date created')),
                ('date_due', models.DateTimeField(default=datetime.datetime(2018, 10, 18, 14, 56, 12, 20322), verbose_name='due date')),
                ('amount_total', models.FloatField(default=0)),
                ('amount_paid', models.FloatField(default=0)),
                ('date_paid', models.DateTimeField(default=datetime.datetime(2019, 9, 13, 14, 56, 12, 20394), verbose_name='date paid')),
                ('paid_in_full', models.BooleanField(default=0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Make',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.Make')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('amount', models.FloatField()),
                ('date_filed', models.DateTimeField(verbose_name='date filed')),
                ('date_paid', models.DateTimeField(default=datetime.datetime(2019, 9, 13, 14, 56, 12, 19509), verbose_name='date paid')),
                ('invoiced', models.BooleanField(default=0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.Customer')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workshop.Employee')),
                ('user', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(default='n/a', max_length=4)),
                ('plate_number', models.CharField(default='n/a', max_length=10)),
                ('color', models.CharField(default='n/a', max_length=50)),
                ('vim', models.CharField(default='n/a', max_length=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workshop.Customer')),
                ('make', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='workshop.Make')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workshop.Model')),
                ('user', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.Vehicle'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='tasks',
            field=models.ManyToManyField(to='workshop.Task'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
