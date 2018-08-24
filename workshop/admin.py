from django.contrib import admin
from .models import Employee, Make, Model, Customer, Task, Invoice, Vehicle


class EmployeeAdmin(admin.ModelAdmin):

    fieldsets = [
                ('Employee', {'fields': ['name']}),
    ]

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Customer)
admin.site.register(Model)
admin.site.register(Make)
admin.site.register(Task)
admin.site.register(Invoice)
admin.site.register(Vehicle)
