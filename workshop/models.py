from django.db import models

# Create your models here .

class Employee(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Make(models.Model):
    name = models.CharField(max_length=50)
    # icon = models.CharField()

    def __str__(self):
        return self.name

class Model(models.Model):
    name = models.CharField(max_length=50)
    make_id = models.ForeignKey(Make, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(max_length=500)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    year = models.CharField(max_length=4)
    model = models.ForeignKey(Model, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    color = models.CharField(max_length=50)
    vim = models.CharField(max_length=10)
    plate_number = models.CharField(max_length=10)

    def __str__(self):
        return "%s %s %s"(self.year, self.model, self.color)

class Task(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
# TODO form classes for labor and parts
    # labor = models.TextField()
    # parts = models.TextField()
    description = models.TextField()
    amount = models.FloatField()
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    date_filed = models.DateTimeField('date filed')
    date_paid = models.DateTimeField('date paid')
    invoiced = models.BooleanField(default='FALSE')

    def __str__(self):
        return "%s %s %s"(self.customer, self.vehicle, self.description)

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField('date created')
    date_due = models.DateTimeField('due date')
    amount_total = models.FloatField()
    amount_paid = models.FloatField()
    tasks = models.ManyToManyField(Task)
    date_paid = models.DateTimeField('date paid')
    paid_in_full = models.BooleanField(default='FALSE')

    def __str__(self):
        return "%s %s"(self.customer, self.total)
