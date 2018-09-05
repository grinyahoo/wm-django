import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.urls import reverse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from .models import Employee, Make, Model, Customer, Vehicle, Task, Invoice
from .forms import AddCustomerForm, AddTaskForm, AddEmployeeForm, AddVehicleForm

# Test view:
def test(request):
    context = {}
    return render(request, 'workshop/test.html', context)
# test

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('workshop:index'))
        else:
            context = {
                'username': form.cleaned_data['username'],
                'form': form,
                'display_errors': True,
            }
            return render(request, 'workshop/register.html', context)
            # return redirect(reverse('workshop:register'))
    else:
        form = UserCreationForm(request.GET)
        context = {
            'form': form,
            'display_errors': False,
        }
        return render(request, 'workshop/register.html', context)

@login_required
def user_logout_view(request):
    logout(request)
    context = {}
    return redirect(reverse('workshop:index'))

@login_required
def login(request):
    return redirect(reverse('workshop:index'))


def index(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user).order_by('-date_filed')
        context = {
            'title': 'Dashboard - %s.' % request.user.username,
            'tasks': tasks,
            'view_name': 'dashboard',
            # 'addCustomerForm': addCustomerForm().as_p(),
            # 'addTaskForm': addTaskForm().as_p(),
        }
        return render(request, 'workshop/index.html', context)
    else:
        return redirect(reverse('login'))

@login_required
def dashboard(request):

    tasks = Task.objects.filter(user=request.user).order_by('-date_filed')
    context = {
        'title': 'Dashboard - %s.' % request.user.username,
        'tasks': tasks,
        'view_name': 'dashboard',
    }
    return render(request, 'workshop/index.html', context)

@login_required
def taskList(request):

    tasks = Task.objects.filter(user=request.user).order_by('-date_filed')
    context = {
        'title': 'Tasks - %s.' % request.user.username,
        'tasks': tasks,
        'view_name': 'tasks',
    }
    return render(request, 'workshop/taskList.html', context)


@login_required
def taskDetail(request, task_id):

    task = get_object_or_404(Task, pk=task_id, user=request.user)
    # task = Task.objects.filter(user=request.user, id=kwargs['task_id'])
    context = {
        'title': 'Task #%s details.'%task.id,
        'task': task,
        'view_name': 'tasks'
    }
    return render(request, 'workshop/taskDetail.html', context)

# @login_required
def ajaxAddTask(request):
    if request.method == "POST":
        form = AddTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.date_filed = datetime.datetime.now()
            task.date_paid = datetime.datetime.now()
            task.save()
            return JsonResponse({'message':'Accepted'})
    else:
        if request.user.is_authenticated:
            context = {
                'path': reverse('workshop:ajaxAddTask'),
                'method': 'post',
                'form': AddTaskForm().as_p(),
            }
            return render(request, 'workshop/modal/addForm.html', context)
        else:
            return HttpResponse(status=403)

@login_required
def customerList(request):

    customers = Customer.objects.filter(user=request.user).order_by('name')
    context = {
        'title': 'My customers',
        'customers': customers,
        'form': AddCustomerForm().as_p(),
        'view_name': 'customers',
    }
    return render(request, 'workshop/customerList.html', context)

@login_required
def customerDetail(request, customer_id):

    customer = get_object_or_404(Customer, pk=customer_id, user=request.user)
    context = {
        'title': 'Customer %s details' % customer.name,
        'customer': customer,
        'view_name': 'customers',
    }
    return render(request, 'workshop/customerDetail.html', context)

@login_required
def ajaxAddCustomer(request):
    if request.POST:
        if request.method == "POST":
            form = AddCustomerForm(request.POST)
            if form.is_valid():
                customer = form.save(commit=False)
                customer.user = request.user
                customer.save()
                return JsonResponse({'message':'Accepted'})
    else:
        context = {
            'path': reverse('workshop:ajaxAddCustomer'),
            'method': 'post',
            'form': AddCustomerForm().as_p(),
        }
        return render(request, 'workshop/modal/addForm.html', context)

@login_required
def vehicleList(request):

    vehicles = Vehicle.objects.filter(user=request.user).order_by('-id')[:50]
    context = {
        'title': 'Vehicles on service',
        'vehicles': vehicles,
        'view_name': 'vehicles',
    }
    return render(request, 'workshop/vehicleList.html', context)

@login_required
def vehicleDetail(request, vehicle_id):

    vehicle = get_object_or_404(Vehicle, pk=vehicle_id, user=request.user)
    context = {
        'title': 'Vehicle %s' % vehicle,
        'vehicle': vehicle,
        'view_name': 'vehicles',
    }
    return render(request, 'workshop/vehicleDetail.html', context)

@login_required
def ajaxAddVehicle(request):
    if request.POST:
        if request.method == "POST":
            form = AddVehicleForm(request.POST)
            if form.is_valid():
                vehicle = form.save(commit=False)
                vehicle.user = request.user
                vehicle.save()
                return JsonResponse({'message':'Accepted'})
    else:
        context = {
            'path': reverse('workshop:ajaxAddVehicle'),
            'method': 'post',
            'form': AddVehicleForm().as_p(),
        }
        return render(request, 'workshop/modal/addForm.html', context)

@login_required
def employeeList(request):

    employees = Employee.objects.filter(user=request.user).order_by('name')
    context = {
        'title' : 'My employees',
        'employees': employees,
        'view_name': 'employees',
    }
    return render(request, 'workshop/employeeList.html', context)

@login_required
def employeeDetail(request, employee_id):


    employee = get_object_or_404(Employee, pk=employee_id, user=request.user)
    context = {
        'title': 'Employee %s' % employee.name,
        'employee': employee,
        'view_name': 'employees',
    }
    return render(request, 'workshop/employeeDetail.html', context)

@login_required
def ajaxAddEmployee(request):
    if request.POST:
        if request.method == "POST":
            form = AddEmployeeForm(request.POST)
            if form.is_valid():
                employee = form.save(commit=False)
                employee.user = request.user
                employee.save()
                return JsonResponse({'message':'Accepted'})
    else:
        context = {
            'path': reverse('workshop:ajaxAddEmployee'),
            'method': 'post',
            'form': AddEmployeeForm().as_p(),
        }
        return render(request, 'workshop/modal/addForm.html', context)

@login_required
def invoiceList(request):

    invoices = Invoice.objects.filter(user=request.user).order_by('-date')[:50]
    context = {
        'title': 'My invoices',
        'invoices': invoices,
        'view_name': 'invoices',
    }
    return render(request, 'workshop/invoiceList.html', context)

@login_required
def invoiceDetail(request, invoice_id):

    invoice = get_object_or_404(Invoice, pk=invoice_id, user=request.user)
    context = {
        'title': 'Invoice #%s' % invoice.id,
        'invoice': invoice,
        'view_name': 'invoices',
    }
    return render(request, 'workshop/invoiceDetail.html', context)
