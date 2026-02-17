from auditlog.registry import auditlog
from . import models 
auditlog.register(models.Product)
auditlog.register(models.Supplier)
auditlog.register(models.Stock)
auditlog.register(models.Income)
auditlog.register(models.Sale)
auditlog.register(models.SaleItem)