# from django.db import models
# from django.contrib.auth import get_user_model
# from django.utils import timezone
#
# User = get_user_model()
#
# class IncomeCategory(models.Model):
#     objects = None
#     name = models.CharField(max_length=100, unique=True)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income_categories')
#
#     class Meta:
#         verbose_name = 'Категория дохода'
#         verbose_name_plural = 'Категории доходов'
#         unique_together = ('name', 'owner')
#
#     def __str__(self):
#         return self.name
#
# class Income(models.Model):
#     objects = None
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     date = models.DateField(default=timezone.now)
#     description = models.TextField(blank=True)
#     category = models.ForeignKey(
#         IncomeCategory,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='incomes'
#     )
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name = 'Доход'
#         verbose_name_plural = 'Доходы'
#         ordering = ['-date']
#
#     def __str__(self):
#         return f"{self.amount} - {self.date}"

from django.db import models

class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"
