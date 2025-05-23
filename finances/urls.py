from django.urls import path
from . import views


urlpatterns = [
    path('incomes/', views.IncomeListCreateView.as_view(), name='income-list'),
    path('incomes/<int:pk>/', views.IncomeDetailView.as_view(), name='income-detail'),
]