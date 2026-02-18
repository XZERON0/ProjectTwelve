from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Product, Supplier, Stock, Income, Sale, SaleItem
@login_required
def operations(request):
    tab = request.GET.get('tab', 'income')
    products = Product.objects.all()
    suppliers = Supplier.objects.all()
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'income':
            return handle_income(request)
        elif form_type == 'sale':
            return handle_sale(request)
    incomes = Income.objects.select_related('product', 'supplier').order_by('-date')[:50]
    sales = Sale.objects.prefetch_related('saleitem_set__product').order_by('-created_at')[:50]
    return render(request, 'operations.html', {
        'tab': tab,
        'products': products,
        'suppliers': suppliers,
        'incomes': incomes,
        'sales': sales,
    })
def handle_income(request):
    """Обработка прихода товара"""
    try:
        product_id = request.POST.get('product')
        supplier_id = request.POST.get('supplier')
        quantity = float(request.POST.get('quantity', 0))
        price = float(request.POST.get('price', 0))
        if not product_id or not supplier_id:
            messages.error(request, 'Выберите товар и поставщика')
            return redirect(f"{request.path}?tab=income")
        if quantity <= 0 or price <= 0:
            messages.error(request, 'Количество и цена должны быть больше нуля')
            return redirect(f"{request.path}?tab=income")
        product = Product.objects.get(id=product_id)
        supplier = Supplier.objects.get(id=supplier_id)
        total_sum = round(quantity * price, 2)

        with transaction.atomic():
            Income.objects.create(
                product=product,
                supplier=supplier,
                quantity=quantity,
                price=price,
                total_sum=total_sum,
            )
            stock, created = Stock.objects.get_or_create(
                product=product,
                defaults={'quantity': 0}
            )
            stock.quantity += int(quantity)
            stock.save()
        messages.success(request, f'Приход оформлен: {product.name} — {quantity} {product.unit}')
    except Product.DoesNotExist:
        messages.error(request, 'Товар не найден')
    except Supplier.DoesNotExist:
        messages.error(request, 'Поставщик не найден')
    except (ValueError, TypeError) as e:
        messages.error(request, f'Ошибка в данных: {e}')
    return redirect(f"{request.path}?tab=income")

def handle_sale(request):
    """Обработка расхода / продажи"""
    product_ids = request.POST.getlist('product[]')
    quantities = request.POST.getlist('quantity[]')
    prices = request.POST.getlist('price[]')
    if not product_ids or not any(product_ids):
        messages.error(request, 'Добавьте хотя бы одну позицию')
        return redirect(f"{request.path}?tab=sale")
    items_data = []
    total_sum = 0
    try:
        for pid, qty_str, price_str in zip(product_ids, quantities, prices):
            if not pid:
                continue
            product = Product.objects.get(id=pid)
            qty = float(qty_str)
            price = float(price_str)
            if qty <= 0 or price <= 0:
                messages.error(request, f'Некорректные данные для {product.name}')
                return redirect(f"{request.path}?tab=sale")
            # Проверка остатка
            try:
                stock = Stock.objects.get(product=product)
                if stock.quantity < qty:
                    messages.error(
                        request,
                        f'Недостаточно на складе: {product.name} — доступно {stock.quantity} {product.unit}'
                    )
                    return redirect(f"{request.path}?tab=sale")
            except Stock.DoesNotExist:
                messages.error(request, f'Товара нет на складе: {product.name}')
                return redirect(f"{request.path}?tab=sale")
            item_total = round(qty * price, 2)
            total_sum += item_total
            items_data.append({
                'product': product,
                'stock': stock,
                'quantity': qty,
                'price': price,
                'total_sum': item_total,
            })
        with transaction.atomic():
            sale = Sale.objects.create(
                user=request.user,
                total_sum=round(total_sum, 2),
            )
            for item in items_data:
                SaleItem.objects.create(
                    sale=sale,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price'],
                    total_sum=item['total_sum'],
                )
                # Списываем со склада
                item['stock'].quantity -= int(item['quantity'])
                item['stock'].save()
        messages.success(request, f'Продажа №{sale.id} оформлена на сумму {round(total_sum, 2)} ₽')
    except Product.DoesNotExist:
        messages.error(request, 'Один из товаров не найден')
    except (ValueError, TypeError) as e:
        messages.error(request, f'Ошибка в данных: {e}')
    return redirect(f"{request.path}?tab=sale")