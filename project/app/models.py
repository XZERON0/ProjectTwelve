from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20)
    unit = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
    def __str__(self):
        return self.name
    
class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Остаток"
        verbose_name_plural = "Остатки"
    def __str__(self):
        return f"{self.product} - остаток - {self.quantity}"
    
class Income(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    total_sum = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Поставка"
        verbose_name_plural = "Поставки"

    def __str__(self):
        return f"Поставка №{self.id} - {self.supplier} - {self.date}"
    
class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_sum = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"

    def __str__(self):
        return f"{self.user} - {self.total_sum} - {self.created_at}"
    
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    total_sum = models.DecimalField(max_digits=5, decimal_places=2)
    class Meta:
        verbose_name = "Товар в продаже"
        verbose_name_plural = "Товары в продаже"

    def __str__(self):
        return f"{self.sale} - {self.product} - {self.quantity} - {self.price} - {self.total_sum}"
