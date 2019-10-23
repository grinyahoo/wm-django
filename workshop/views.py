import datetime, json, time
from datetime import date, timedelta
from urllib.request import urlopen
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from django.template import loader
from django.db.models import Q, Count, Sum
from django.utils.decorators import method_decorator

from django.contrib import auth
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Employee, Make, Model, Customer, Vehicle, Task, Invoice
from .forms import CustomerForm, TaskForm, EmployeeForm, VehicleForm, InvoiceForm


# TODO: generic views, ajax mixin.
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

    tasks = Task.objects.filter(user=request.user).order_by('-date_filed')
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

    today = date.today()
    week = datetime.datetime.strptime(
        "{}-W{}".format(today.year, today.isocalendar()[1]) + '-1', 
        "%Y-W%W-%w"
        ) + datetime.timedelta(days=-7)
    context = {
        'title': 'Dashboard - %s.' % request.user.username,
        'invoices': invoices,
        'view_name': 'dashboard',
        'customers': customers,
        'totals': totals,
        'flow': {
            'day': tasks.filter(
                date_filed__year=today.year,
                date_filed__month=today.month,
                date_filed__day=today.day,
                ).aggregate(Sum('amount')),
            'week': tasks.filter(
                date_filed__gte=week
                ).aggregate(Sum('amount')),
            'month': tasks.filter(
                date_filed__year=today.year,
                date_filed__month=today.month
                ).aggregate(Sum('amount')),
        },
        'tasks': tasks,
    }
    return render(request, 'workshop/index.html', context)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = "workshop/taskList.html"
    paginate_by = 50

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user
            ).order_by('-date_filed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'WM - list of tasks.'
        # context["view_name"] = "dashboard"
        return context

  
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "workshop/taskCreate.html"


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = "workshop/taskDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context[""] = 
        return context
    


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
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.date_filed = datetime.datetime.now()
            task.date_paid = datetime.datetime.now()
            task.save()
            return JsonResponse({'message':'Accepted'})
    else:
        if request.user.is_authenticated:
            vehicles = Vehicle.objects.filter(
                user=request.user
            )
            # form = TaskForm().loadVehicles(request.user)
            context = {
                'path': reverse('workshop:ajaxAddTask'),
                'method': 'post',
                'form': TaskForm(),
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
        'form': CustomerForm().as_p(),
        'view_name': 'customers',
    }
    return render(request, 'workshop/customerList.html', context)

@login_required
def customerDetail(request, customer_id):

    customer = get_object_or_404(Customer, pk=customer_id, user=request.user)
    tasks = Task.objects.filter(customer=customer)
    vehicles = Vehicle.objects.filter(customer=customer)
    invoices = Invoice.objects.filter(customer=customer)

    form = CustomerForm(instance=customer)
    if request.POST:
        form = CustomerForm(request.POST or None, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()

    context = {
        'title': 'Customer %s details' % customer.name,
        'customer': customer,
        'vehicles': vehicles,
        'tasks': tasks,
        'invoices': invoices,
        'view_name': 'customers',
        'form': form
    }
    return render(request, 'workshop/customerDetail.html', context)

@login_required
def ajaxAddCustomer(request):
    if request.POST:
        if request.method == "POST":
            form = CustomerForm(request.POST)
            if form.is_valid():
                customer = form.save(commit=False)
                customer.user = request.user
                customer.save()
                return JsonResponse({'message':'Accepted'})
    else:
        context = {
            'path': reverse('workshop:ajaxAddCustomer'),
            'method': 'post',
            'form': CustomerForm(),
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
    tasks = Task.objects.filter(vehicle=vehicle).order_by('-date_filed')

    form = VehicleForm(instance=vehicle)
    if request.POST:
        form = VehicleForm(request.POST or None, instance=vehicle)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user
            vehicle.save()

    context = {
        'title': 'Vehicle %s' % vehicle,
        'vehicle': vehicle,
        'tasks': tasks,
        'view_name': 'vehicles',
        'form': form,
    }
    return render(request, 'workshop/vehicleDetail.html', context)

@login_required
def ajaxAddVehicle(request):
    if request.POST:
        if request.method == "POST":
            form = VehicleForm(request.POST)
            if form.is_valid():
                vehicle = form.save(commit=False)
                vehicle.user = request.user
                vehicle.save()
                return JsonResponse({'message':'Accepted'})
    else:
        context = {
            'path': reverse('workshop:ajaxAddVehicle'),
            'method': 'post',
            'form': VehicleForm(),
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

# TODO use messages framework  
@login_required
def employeeDetail(request, employee_id):

    messages = {}

    employee = get_object_or_404(Employee, pk=employee_id, user=request.user)
    form = EmployeeForm(instance=employee)
    if request.POST:
        form = EmployeeForm(request.POST or None, instance=employee)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.user = request.user
            employee.save()
            messages['success'] = "Employee data saved successfuly."
        else:
            messages['warning'] = "Form is not vaild. Employee data was not saved."      
    context = {
        'title': 'Employee %s' % employee.name,
        'employee': employee,
        'view_name': 'employees',
        'form': form,
        'messages': messages
    }
    return render(request, 'workshop/employeeDetail.html', context)

@login_required
def ajaxAddEmployee(request):
    if request.POST:
        if request.method == "POST":
            form = EmployeeForm(request.POST)
            if form.is_valid():
                employee = form.save(commit=False)
                employee.user = request.user
                employee.save()
                return JsonResponse({'message':'Accepted'})
    else:
        context = {
            'path': reverse('workshop:ajaxAddEmployee'),
            'method': 'post',
            'form': EmployeeForm(),
        }
        return render(request, 'workshop/forms/employee.html', context)

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
            form = InvoiceForm(request.POST)
            if form.is_valid():
                invoice = form.save(commit=False)
                invoice.user = request.user
                tasks = form.cleaned_data['tasks']
                invoice.amount_total = tasks.aggregate(Sum('amount'))['amount__sum']
                invoice.save()
                return JsonResponse({'message': ""})
            else:
                return JsonResponse({'message': form.errors })
    else:
        if request.GET['customer']:
            context = {
                'path': reverse('workshop:ajaxAddInvoice'),
                'method': 'post',
                'form': InvoiceForm(q={'user':request.user, 'customer':request.GET['customer']}),
                # 'form': InvoiceForm(),

            }
            return render(request, 'workshop/modal/addForm.html', context)
        else:
            return JsonResponse({'message': 'no customer' })
