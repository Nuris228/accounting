from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Sum
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from models import Income, IncomeCategory
from serializers import (
    IncomeSerializer,
    IncomeCategorySerializer,
    IncomeSummarySerializer
)

User = get_user_model()


class IncomeCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = IncomeCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return IncomeCategory.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IncomeCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return IncomeCategory.objects.filter(owner=self.request.user)


class IncomeListCreateView(generics.ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Income.objects.filter(owner=self.request.user)

        # Фильтрация по дате
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        # Фильтрация по категории
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset.order_by('-date')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IncomeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(owner=self.request.user)


def get(request):
    month = request.query_params.get('month')
    year = request.query_params.get('year', datetime.now().year)

    incomes = Income.objects.filter(
        owner=request.user,
        date__year=year
    )

    if month:
        incomes = incomes.filter(date__month=month)

    total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0

    category_totals = incomes.values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')

    category_totals_dict = {
        item['category__name']: item['total']
        for item in category_totals
        if item['category__name']
    }

    data = {
        'total_income': total_income,
        'category_totals': category_totals_dict,
        'month': month,
        'year': year
    }

    serializer = IncomeSummarySerializer(data)
    return Response(serializer.data)


class IncomeSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]


class IncomeDetailView:
    pass