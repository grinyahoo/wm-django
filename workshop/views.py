import datetime, json, time
from urllib.request import urlopen
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views import generic
from django.urls import reverse
from django.template import loader
from django.db.models import Q, Count
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from .models import Employee, Make, Model, Customer, Vehicle, Task, Invoice
from .forms import AddCustomerForm, AddTaskForm, AddEmployeeForm, AddVehicleForm, AddInvoiceForm

# Test view:
def test(request):

    v_types = ['car', 'truck', 'mpv', 'bus']
    for t in v_types:
        raw_makes = json.loads(urlopen('https://vpic.nhtsa.dot.gov/api/vehicles/GetMakesForVehicleType/%s?format=json'%t).read().decode())
        # makes.append(raw_makes['Results'])
        for m in raw_makes['Results']:
            mk = Make(id=m['MakeId'], name=m['MakeName'])

            try:
                mk.save()
            except Exception as e:
                pass

    for make in Make.objects.all():
        raw_models = json.loads(urlopen('https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeId/%s?format=json'%make.id).read().decode())
        for m in raw_models['Results']:
            md = Model(id=m['Model_ID'], name=m['Model_Name'], make=make)
            try:
                md.save()
            except Exception as e:
                pass
        time.sleep(.1)

    return HttpResponse('Done')


    # return render(request, 'workshop/test.html', context)

# # test

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

@login_required
def index(request):
    return redirect(reverse('workshop:dashboard'))

@login_required
def dashboard(request):

    tasks = Task.objects.filter(user=request.user).order_by('-date_filed')[:20]
    customers = Customer.objects.filter(
                                    user=request.user,
                                    task__invoiced=0
                                    ).annotate(
                                    tasks_total=Count('task')
                                    ).annotate(
                                    tasks_uninvoiced=Count('task', filter=Q(task__invoiced=0))
                                    )
    invoices = Invoice.objects.filter(user=request.user).order_by('-date')[:20]
    totals = {
        'customers': Customer.objects.filter(user=request.user).count(),
        'vehicles': Vehicle.objects.filter(user=request.user).count(),
        'invoices': Invoice.objects.filter(user=request.user).count(),
        'tasks': Task.objects.filter(user=request.user).count()
    }
    context = {
        'title': 'Dashboard - %s.' % request.user.username,
        'tasks': tasks,
        'invoices': invoices,
        'view_name': 'dashboard',
        'customers': customers,
        'totals': totals,
    }
    return render(request, 'workshop/index.html', context)

@login_required
def taskList(request):

    tasks_all = Task.objects.filter(user=request.user).order_by('-date_filed')
    context = {
        'title': 'Tasks - %s.' % request.user.username,
        'tasks': tasks_all,
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
            form = AddTaskForm().loadVehicles(request.user)
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
    tasks = Task.objects.filter(customer=customer)
    vehicles = Vehicle.objects.filter(customer=customer)
    invoices = Invoice.objects.filter(customer=customer)
    context = {
        'title': 'Customer %s details' % customer.name,
        'customer': customer,
        'vehicles': vehicles,
        'tasks': tasks,
        'invoices': invoices,
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
    # Implement vehicles by customer .annotate
    # vehicles_by_customer = Customer.objects.filter(user=request.user).annotate(vehicles='vehicle')
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
    tasks = Task.objects.filter(vehicle=vehicle).order_by('-date_filed')
    context = {
        'title': 'Vehicle %s' % vehicle,
        'vehicle': vehicle,
        'tasks': tasks,
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
    form = AddEmployeeForm(instance=employee)
    context = {
        'title': 'Employee %s' % employee.name,
        'employee': employee,
        'view_name': 'employees',
        'form': form
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
    tasks_uninvoiced = Task.objects.filter(user=request.user, invoiced=0)
    # customers = Customer.filter(user=request.user).order_by('name')


    context = {
        'title': 'My invoices',
        'invoices': invoices,
        'view_name': 'invoices',
        'tasks_uninvoiced': tasks_uninvoiced,
        'tasks_uninvoiced_count': tasks_uninvoiced.count(),
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

@login_required
def ajaxAddInvoice(request):
    if request.POST:
        if request.method == "POST":
            form = AddInvoiceForm(request.POST)
            if form.is_valid():
                invoice = form.save(commit=False)
                invoice.user = request.user
                invoice.save()
                return JsonResponse({'message':'Accepted'})
            else:
                return JsonResponse({'message':'Form is not valid.'})
    else:
        context = {
            'path': reverse('workshop:ajaxAddInvoice'),
            'method': 'post',
            'form': AddInvoiceForm(q={'user':request.user, 'customer':request.GET['customer']}).as_p(),
        }
        return render(request, 'workshop/modal/addForm.html', context)
