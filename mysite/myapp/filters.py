import django_filters
from .models import Expense, Category

class ExpenseFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter()
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Expense
        fields = ['date', 'category']
