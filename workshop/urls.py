from django.urls import path
from . import views

app_name = 'workshop'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('login', views.login, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('logout', views.user_logout_view, name='logout'),
    path('dashboard', views.dashboard, name = 'dashboard'),
    #
    path('tasks', views.taskList, name='taskList'),
    path('tasks/<int:task_id>', views.taskDetail, name='taskDetail'),
    path('ajax/addTask', views.ajaxAddTask, name='ajaxAddTask'),
    #
    path('vehicles/', views.vehicleList, name='vehicleList'),
    path('vehicles/<int:vehicle_id>', views.vehicleDetail, name='vehicleDetail'),
    path('ajax/addVehicle', views.ajaxAddVehicle, name='ajaxAddVehicle'),
    #
    path('customers/', views.customerList, name='customerList'),
    path('customer/<int:customer_id>', views.customerDetail, name='customerDetail'),
    path('ajax/addCustomer', views.ajaxAddCustomer, name='ajaxAddCustomer'),
    #
    path('employees/', views.employeeList, name='employeeList'),
    path('employees/<int:employee_id>', views.employeeDetail, name='employeeDetail'),
    path('ajax/addEmployee', views.ajaxAddEmployee, name='ajaxAddEmployee'),
    #
    path('invoices/', views.invoiceList, name='invoiceList'),
    path('invoices/<int:invoice_id>', views.invoiceDetail, name='invoiceDetail'),
    path('ajax/addInvoice', views.ajaxAddInvoice, name='ajaxAddInvoice'),
    #
    path('test/', views.test, name = 'test'),

]
