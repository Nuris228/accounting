from django.contrib import admin
from .models import Income, IncomeCategory

@admin.register(IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'date', 'category', 'owner')
    list_filter = ('category', 'date')
    search_fields = ('description',)