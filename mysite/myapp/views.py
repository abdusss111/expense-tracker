from django.db.models import Sum
import datetime


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Expense, Category, GroupExpense
from .forms import ExpenseForm
from .filters import ExpenseFilter

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    expense_filter = ExpenseFilter(request.GET, queryset=expenses)

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')

    expense_form = ExpenseForm()
    return render(request, 'expense_list.html', {
        'expense_form': expense_form,
        'filter': expense_filter,
    })

@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        Category.objects.create(name=name, user=request.user)
        return redirect('add_category')
    return render(request, 'add_category.html')

@login_required
def add_group_expense(request):
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        users = request.POST.getlist('users')
        group_expense = GroupExpense.objects.create(name=name, amount=amount, date=timezone.now())
        group_expense.users.set(users)
        return redirect('group_expense_list')

    from django.contrib.auth.models import User
    users = User.objects.all()
    return render(request, 'add_group_expense.html', {'users': users})

@login_required
def group_expense_list(request):
    expenses = GroupExpense.objects.all()
    return render(request, 'group_expense_list.html', {'expenses': expenses})


def index(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()

    expenses = Expense.objects.all()
    total_expenses = expenses.aggregate(Sum('amount'))

    last_year = datetime.date.today() - datetime.timedelta(days=365)
    yearly_sum = Expense.objects.filter(date__gt=last_year).aggregate(Sum('amount'))

    last_month = datetime.date.today() - datetime.timedelta(days=30)
    monthly_sum = Expense.objects.filter(date__gt=last_month).aggregate(Sum('amount'))

    last_week = datetime.date.today() - datetime.timedelta(days=7)
    weekly_sum = Expense.objects.filter(date__gt=last_week).aggregate(Sum('amount'))

    daily_sums = Expense.objects.values('date').order_by('date').annotate(sum=Sum('amount'))
    categorical_sums = Expense.objects.values('category').order_by('category').annotate(sum=Sum('amount'))

    expense_form = ExpenseForm()
    return render(request, 'myapp/index.html', {
        'expense_form': expense_form,
        'expenses': expenses,
        'total_expenses': total_expenses,
        'yearly_sum': yearly_sum,
        'monthly_sum': monthly_sum,
        'weekly_sum': weekly_sum,
        'daily_sums': daily_sums,
        'categorical_sums': categorical_sums
    })

def edit(request, id):
    expense = Expense.objects.get(id=id)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')
    expense_form = ExpenseForm(instance=expense)
    return render(request, 'myapp/edit.html', {'expense_form': expense_form})

def delete(request, id):
    if request.method == "POST" and 'delete' in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')

