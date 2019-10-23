import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer, Employee, Vehicle, Task, Invoice
# TODO: make timezone aware

YEARS = tuple((x,x) for x in range(datetime.date.today().year, 1950, -1))

class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['name', 'address', 'city', 'state', 'zip', 'phone']
        widgets = {
            'address': forms.TextInput()
        }

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['customer', 'vehicle', 'description', 'amount', 'employee']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        exclude = ['user']
        widgets = {
            'notes': forms.Textarea()
        }
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Add employee',
                'name', 
                'cost_per_hour', 
                'phone', 
                'notes'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class="button white"),

            )
        )
        super(EmployeeForm, self).__init__(*args, **kwargs)

class VehicleForm(forms.ModelForm):

    class Meta:
        model = Vehicle
        exclude = ['user']
        widgets = {
            'year': forms.Select(choices=YEARS),
        }

class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ['customer', 'tasks',]
        widgets = {
            'customer': forms.HiddenInput(),
            'tasks': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, q={}, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        if q:
            self.fields['tasks'].queryset = Task.objects.filter(user=q['user'], customer=q['customer'], invoiced=0)
            self.initial['customer'] = Customer.objects.get(user=q['user'], id=q['customer']).id


class CustomAuthenticationForm(AuthenticationForm):

    # username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username'}))
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
