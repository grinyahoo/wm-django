from django.db import models
from django.contrib.auth.models import User
import datetime

# helper functions

def now_plus_days(days):
    return datetime.datetime.now() + datetime.timedelta(days=days)

class Employee(models.Model):
    name = models.CharField(max_length=200)
    cost_per_hour = models.FloatField(default=0)
    phone = models.CharField(max_length=15, null=True)
    notes = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=2)

    def __str__(self):
        return self.name

class Make(models.Model):
    name = models.CharField(max_length=50)
    # icon = models.CharField()

    def __str__(self):
        return self.name

class Model(models.Model):
    name = models.CharField(max_length=50)
    make = models.ForeignKey(Make, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(max_length=500)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    phone = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=2)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    year = models.CharField(max_length=4, default='n/a')
    make = models.ForeignKey(Make, on_delete=models.PROTECT, default=1)
    model = models.ForeignKey(Model, on_delete=models.PROTECT)
    plate_number = models.CharField(max_length=10, default='n/a')
    color = models.CharField(max_length=50, default='n/a')
    vim = models.CharField(max_length=10, default='n/a')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=2)

    def __str__(self):
        return "%s %s %s" % (self.year, self.make, self.model)

class Task(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
# TODO implement classes for labor and parts
    # labor = models.TextField()
    # parts = models.TextField()
    description = models.TextField()
    amount = models.FloatField()
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    date_filed = models.DateTimeField('date filed')
    date_paid = models.DateTimeField('date paid', default=now_plus_days(360))
    invoiced = models.BooleanField(default=0)
    # invoice = models.ForeignKey(Invoice, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=2)

    def __str__(self):
        # return "%s %s %s" % (self.customer, self.vehicle, self.description)
        return "%s %s" % (self.vehicle, self.description)

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField('date created', default=datetime.datetime.now())
    date_due = models.DateTimeField('due date', default=now_plus_days(30))
    amount_total = models.FloatField(default=0)
    amount_paid = models.FloatField(default=0)
    tasks = models.ManyToManyField(Task)
    date_paid = models.DateTimeField('date paid', default=now_plus_days(360))
    paid_in_full = models.BooleanField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.customer, self.amount_total)
