"""
URL configuration for Inventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from IMS_APP import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('main_menu/', views.main_menu_page, name='main_menu_page'),
    path('supplier_page/', views.supplier_page, name='supplier_page'),
    path('delete_supplier/<int:id>/', views.delete_sup, name='delete_sup'),
    path('update_supplier/<int:id>/', views.update_sup, name='update_sup'),
    path('category/', views.category_page, name='category_page'),
    path('delete_cat/<int:id>/', views.delete_cat, name='delete_cat'),
    path('product/', views.product_page, name='product_page'),
    path('delete_pro/<int:id>/', views.delete_pro, name='delete_pro'),
    path('update_pro/<int:id>/', views.update_pro, name='update_pro'),
    path('employee/', views.employee_page, name='employee_page'),
    path('delete_emp/<int:id>/', views.delete_emp, name='delete_emp'),
    path('update_emp/<int:id>/', views.update_emp, name='update_emp'),
    path('customer/', views.customer_page, name='customer_page'),
    path('billing_page/', views.billing_page, name='billing_page'),
    path('process_cart/<int:id>/', views.process_cart, name='process_cart'),
    path('cart/', views.cart_page, name='cart_page'),
    path('delete_cart/<int:id>/', views.delete_cart, name='delete_cart'),
    path('bill/', views.bill, name='bill'),
    path('sales_page/', views.sales_page, name='sales_page'),
    path('getsales/<int:id>/', views.getsales, name='getsales'),
]