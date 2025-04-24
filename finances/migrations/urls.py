from django.urls import path
from .views import (
    IncomeCategoryListCreateView,
    IncomeListCreateView,
    IncomeDetailView
)

urlpatterns = [
    path('categories/', IncomeCategoryListCreateView.as_view(), name='income-categories'),
    path('incomes/', IncomeListCreateView.as_view(), name='income-list'),
    path('incomes/<int:pk>/', IncomeDetailView.as_view(), name='income-detail'),
]