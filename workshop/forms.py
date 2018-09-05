import datetime
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer, Employee, Vehicle, Task, Invoice
# from django.utils import timezone

YEARS = tuple((x,x) for x in range(2018, 1950, -1)) # TODO flexible YEARS

class AddCustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['name', 'address', 'city', 'state', 'zip', 'phone']

class AddTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['customer', 'vehicle', 'description', 'amount', 'employee']

class AddEmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['name']

class AddVehicleForm(forms.ModelForm):

    class Meta:
        model = Vehicle
        fields = ['customer', 'year', 'make', 'model', 'plate_number', 'color', 'vim']
        widgets = {
            'year': forms.Select(choices=YEARS),
        }

class CustomAuthenticationForm(AuthenticationForm):

    # username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username'}))
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
