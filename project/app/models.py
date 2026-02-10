from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=20)

    def __str__(self):
        return self.username
    
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20)
    unit = models.CharField(max_length=20)
    created_at = models.DateTimeField

    def __str__(self):
        return self.name
    
class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField
    updated_at = models.DateTimeField

    def __str__(self):
        return f"{self.product} - остаток - {self.quantity}"
    
class Income(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.FloatField
    price = models.DecimalField(max_digits=5, decimal_places=2)
    total_sum = models.DecimalField(max_digits=5, decimal_places=2)
    accepted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField

    def __str__(self):
        return f"Поставка №{self.id} - {self.supplier} - {self.date}"
    
class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_sum = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField

    def __str__(self):
        return f"{self.user} - {self.total_sum} - {self.created_at}"
    
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField
    price = models.DecimalField(max_digits=5, decimal_places=2)
    total_sum = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.sale} - {self.product} - {self.quantity} - {self.price} - {self.total_sum}"