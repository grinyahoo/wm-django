from django.urls import path
from . import views

app_name = 'workshop'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('task/<int:task_id>', views.taskDetail, name='taskDetail'),
    path('register/', views.register, name = 'register'),
    path('vehicles/', views.vehicleList, name='vehicleList'),
    path('vehicle/<int:vehicle_id>', views.vehicleDetail, name='vehicleDetail'),
    path('customers/', views.customerList, name='customerList'),
    path('customer/<int:customer_id>', views.customerDetail, name='customerDetail'),
    path('employees/', views.employeeList, name='employeeList'),
    path('employee/<int:employee_id>', views.employeeDetail, name='employeeDetail'),
    path('invoices/', views.invoiceList, name='invoiceList'),
    path('invoice/<int:invoice_id>', views.invoiceDetail, name='invoiceDetail'),
    path('test/', views.test, name = 'test'),

]
