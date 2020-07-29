from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('applications', views.application, name='application'),
    path('storage', views.storage, name='storage'),
    path('workflow', views.workflow, name="workflow"),
    path('new-workflow', views.new_workflow, name="new_workflow"),
    path('add_workflow', views.add_workflow, name="add_workflow"),
    path('form', views.form, name="form"),
    path('new-form', views.new_form, name="new_form"),
    path('add_form', views.add_form, name="add_form"),
    path('new_document', views.new_document, name="new_document")
]
