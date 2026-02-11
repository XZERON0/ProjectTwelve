from django.contrib import admin

# from .models import User
from .models import Supplier, Product, Stock, Income, Sale, SaleItem
#! Убрал класс User, так как 
#! он уже есть в Django и не нужно его дублировать
# admin.site.register(User)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(Income)
admin.site.register(Sale)
admin.site.register(SaleItem)