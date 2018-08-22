from django.shortcuts import render
from django.views import generic

from .models import Employee, Make, Model, Customer, Vehicle, Task, Invoice

class IndexView(generic.ListView):
    template_name = 'workshop/index.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        """ Return all tasks """
        return Task.objects.all().order_by('-date_filed')
