from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='documents-home'),
    path('instantiate-contract/', views.instantiate_contract, name='instantiate_contract'),
    path('sign-contract/<str:envelope_id>/', views.sign_contract, name='sign_contract'),
    path('success/', views.success, name='success'),
]
