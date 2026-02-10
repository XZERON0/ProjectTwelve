from django.contrib import admin

from .models import User, Supplier, Product, Stock, Income, Sale, SaleItem

admin.site.register(User)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(Income)
admin.site.register(Sale)
admin.site.register(SaleItem)