from django.urls import path
from . import views


urlpatterns = [
    path('', views.test, name='dev-test'),
    path('interfaces/', views.interfaces, name='dev-ints'),
]