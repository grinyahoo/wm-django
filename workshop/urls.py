from django.urls import path
from . import views

app_name = 'workshop'
urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
]
