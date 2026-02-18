from django.shortcuts import render, redirect
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Stock, Income, Sale, SaleItem
def reports(request):
    if not request.user.is_authenticated:
        return redirect('login')
    period = request.GET.get('period', 'week')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    now = timezone.now()
    if period == 'day':
        start_date = now - timedelta(days=1)
        end_date = now
        period_label = 'За день'
    elif period == 'week':
        start_date = now - timedelta(weeks=1)
        end_date = now
        period_label = 'За неделю'
    elif period == 'month':
        start_date = now - timedelta(days=30)
        end_date = now
        period_label = 'За месяц'
    elif period == 'year':
        start_date = now - timedelta(days=365)
        end_date = now
        period_label = 'За год'
    elif period == 'custom' and date_from and date_to:
        from datetime import datetime
        start_date = timezone.make_aware(datetime.strptime(date_from, '%Y-%m-%d'))
        end_date = timezone.make_aware(datetime.strptime(date_to, '%Y-%m-%d').replace(hour=23, minute=59))
        period_label = f'{date_from} — {date_to}'
    else:
        start_date = now - timedelta(weeks=1)
        end_date = now
        period_label = 'За неделю'
    sales = Sale.objects.filter(created_at__range=(start_date, end_date))
    total_sales_sum = sales.aggregate(total=Sum('total_sum'))['total'] or 0
    total_sales_count = sales.count()
    incomes = Income.objects.filter(date__range=(start_date, end_date))
    total_income_sum = incomes.aggregate(total=Sum('total_sum'))['total'] or 0
    total_income_count = incomes.count()
    top_products = (
        SaleItem.objects
        .filter(sale__created_at__range=(start_date, end_date))
        .values('product__name')
        .annotate(total_qty=Sum('quantity'), total_sum=Sum('total_sum'))
        .order_by('-total_qty')[:10]
    )
    stocks = Stock.objects.select_related('product').all()
    context = {
        'period': period,
        'period_label': period_label,
        'date_from': date_from or '',
        'date_to': date_to or '',
        'start_date': start_date,
        'end_date': end_date,
        'total_sales_sum': total_sales_sum,
        'total_sales_count': total_sales_count,
        'total_income_sum': total_income_sum,
        'total_income_count': total_income_count,
        'top_products': top_products,
        'stocks': stocks,
        'period_choices': [
        ('day', 'День'),
        ('week', 'Неделя'),
        ('month', 'Месяц'),
        ('year', 'Год'),
    ],
    }
    return render(request, 'reports/reports.html', context)