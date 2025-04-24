from rest_framework import serializers
from models import Income, IncomeCategory
from django.contrib.auth import get_user_model

User = get_user_model()

class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        fields = ['id', 'name']
        read_only_fields = ['id']


def validate_amount(value):
    if value <= 0:
        raise serializers.ValidationError("Сумма должна быть положительной")
    return value


class IncomeSerializer(serializers.ModelSerializer):
    category = IncomeCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=IncomeCategory.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Income
        fields = [
            'id', 'amount', 'date', 'description',
            'category', 'category_id', 'owner',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

class IncomeSummarySerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    category_totals = serializers.DictField(
        child=serializers.DecimalField(max_digits=10, decimal_places=2)
    )
    month = serializers.CharField()
    year = serializers.IntegerField()