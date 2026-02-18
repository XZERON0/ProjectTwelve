from django.urls import path 
from . import views
from . import views_reports
from . import views_operations
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout_user'),
    ## goods
    path('goods/', views.goods, name='goods'),
    ## reports
    path('reports/', views_reports.reports, name='reports'),
    ## suppliers
    path('suppliers/', views.suppliers, name='suppliers'),    
    ## operations
    path('operations/', views_operations.operations, name='operations'),
]
