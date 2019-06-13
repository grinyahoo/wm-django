import datetime
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer, Employee, Vehicle, Task, Invoice
# from django.utils import timezone

YEARS = tuple((x,x) for x in range(datetime.date.today().year, 1950, -1))

## Need
## form to pick customers
## form to pick make -> return models by make
##

class AddCustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['name', 'address', 'city', 'state', 'zip', 'phone']
        widgets = {
            'address': forms.TextInput()
        }

class AddTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['customer', 'vehicle', 'description', 'amount', 'employee']

    # def __init__(self, *args, **kwargs):
    #     super(AddTaskForm, self).__init__(*args, **kwargs)

    def loadVehicles(self, user):
        self.fields['vehicle'].queryset = Vehicle.objects.filter(user=user)
        # self.fields['vehicle'].queryset = Vehicle.objects.all()

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

class AddInvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ['customer', 'tasks',]
        widgets = {
            'customer': forms.HiddenInput(),
            'tasks': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, q={}, **kwargs):
        super(AddInvoiceForm, self).__init__(*args, **kwargs)
        if q:
            self.fields['tasks'].queryset = Task.objects.filter(user=q['user'], customer=q['customer'], invoiced=0)
            self.initial['customer'] = Customer.objects.get(user=q['user'], id=q['customer']).id


class CustomAuthenticationForm(AuthenticationForm):

    # username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username'}))
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
