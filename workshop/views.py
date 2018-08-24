from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login
from django.contrib import auth
from .models import Employee, Make, Model, Customer, Vehicle, Task, Invoice

# Test view:
def test(request):
    context = {}
    return render(request, 'workshop/test.html', context)
# test

def goLogin(request):
    redirect(reverse('login'), {'next': request})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('index'))
        else:
            return redirect(reverse('register'))
    else:
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'workshop/register.html', context)

def index(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user).order_by('-date_filed')
        context = {
            'title': 'Dashboard - %s.' % request.user.username,
            'tasks': tasks,
        }
        return render(request, 'workshop/index.html', context)
    else:
        return goLogin(request)

def taskDetail(request, tasks_id):
    if request.user.is_authenticated:
        task = Task.objects.filter(user=request.user, id=task_id)
        context = {
            'title': 'Task #%s details.'%task.id,
            'task': task,
        }
        return render(request, 'workshop/taskDetail.html', context)
    else:
        return goLogin(request)

def customerList(request):
    if request.user.is_authenticated:
        customers = Customer.objects.filter(user=request.user).order_by('name')
        context = {
            'title': 'My customers',
            'customers': customers,
        }
        return render(request, 'workshop/customerList.html', context)
    else:
        return goLogin(request)

def customerDetail(request, customer_id):
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user, id=customer_id)
        context = {
            'title': 'Customer %s details' % customer.name,
            'customer': customer,
        }
        return render(request, 'workshop/customerDetail.html', context)
    else:
        return goLogin(request)

def vehicleList(request):
    if request.user.is_authenticated:
        vehicles = Vehicle.objects.filter(user=request.user).order_by('-id')[:50]
        context = {
            'title': 'Vehicles on service',
            'vehicles': vehicles,
        }
        return render(request, 'workshop/vehicleList.html', context)
    else:
        return goLogin(request)

def vehicleDetail(request, vehicle_id):
    if request.user.is_authenticated:
        vehicle = Vehicle.objects.filter(user=request.user, id=vehicle_id)
        context = {
            'title': 'Vehicle %s' % vehicle,
            'vehicle': vehicle,
        }
        return render(request, 'workshop/vehicleDetail.html', context)
    else:
        return goLogin(request)

def employeeList(request):
    if request.user.is_authenticated:
        employees = Employee.objects.filter(user=request.user).order_by('name')
        context = {
            'title' : 'My employees',
            'employees': employees,
        }
        return render(request, 'workshop/employeeList.html', context)
    else:
        return goLogin(request)

def employeeDetail(request, employee_id):
    if request.user.is_authenticated:
        employee = Employee.objects.filter(user=request.user, id=employee_id)
        context = {
            'title': 'Employee %s' % employee.name,
            'employee': employee,
        }
        return render(request, 'workshop/employeeDetail.html', context)
    else:
        return goLogin(request)

def invoiceList(request):
    if request.user.is_authenticated:
        invoices = Invoice.objects.filter(user=request.user).order_by('-date')[:50]
        context = {
            'title': 'My invoices',
            'invoices': invoices,
        }
        return render(request, 'workshop/invoiceList.html', context)
    else:
        return goLogin(request)

def invoiceDetail(request, invoice_id):
    if request.user.is_authenticated:
        invoice = Invoice.objects.filter(user=request.user, id=invoice_id)
        context = {
            'title': 'Invoice #%s' % invoice.id,
            'invoice': invoice,
        }
        return render(request, 'workshop/invoiceDetail.html', context)
    else:
        return goLogin(request)
