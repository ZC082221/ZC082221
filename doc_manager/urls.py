# doc_manager/urls.py
from django.urls import path
from . import views

app_name = 'doc_manager'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sop/create/', views.create_sop, name='create_sop'),
    path('kanban/create/', views.create_kanban_card, name='create_kanban_card'),
    # Route for the simulated approval test
    path('approve_test/<str:simulated_doc_id>/', views.approve_document_test_view, name='approve_document_test'),
    path('not_authorized/', views.not_authorized_view, name='not_authorized'),
]
