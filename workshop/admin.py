from django.contrib import admin
from .models import Employee, Make, Model


class EmployeeAdmin(admin.ModelAdmin):

    fieldsets = [
                ('Employee', {'fields': ['name']}),
    ]

admin.site.register(Employee, EmployeeAdmin)
