from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('applications', views.application, name='application'),
    path('storage', views.storage, name='storage')
]