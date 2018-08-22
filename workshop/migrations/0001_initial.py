# Generated by Django 2.1 on 2018-08-20 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='date created')),
                ('date_due', models.DateTimeField(verbose_name='due date')),
                ('amount_total', models.FloatField()),
                ('amount_paid', models.FloatField()),
                ('date_paid', models.DateTimeField(verbose_name='date paid')),
                ('paid_in_full', models.BooleanField(default='FALSE')),
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
                ('make_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.Make')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('amount', models.FloatField()),
                ('date_filed', models.DateTimeField(verbose_name='date filed')),
                ('date_paid', models.DateTimeField(verbose_name='date paid')),
                ('invoiced', models.BooleanField(default='FALSE')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.Customer')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workshop.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
                ('color', models.CharField(max_length=50)),
                ('vim', models.CharField(max_length=10)),
                ('plate_number', models.CharField(max_length=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workshop.Customer')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workshop.Model')),
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
    ]
