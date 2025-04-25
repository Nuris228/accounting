from django.urls import path
from finances.views import IncomeListCreateView, IncomeDetailView  # Явный импорт

urlpatterns = [
    path('incomes/', IncomeListCreateView.as_view(), name='income-list'),
    path('incomes/<int:pk>/', IncomeDetailView.as_view(), name='income-detail'),
]