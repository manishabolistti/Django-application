"""
URL configuration for demoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from .views import home,about,demo
from demoapp.views import home as demoapp_home,example_view,bill_data,print_bill,get_items,navbar_view,dashboard_view,stock_view,item_tables_view
from django.conf.urls.static import static
from django.conf import  settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('demoapp/', demoapp_home, name='demoapp_home'),
    path('example/', example_view, name='example'),
    path('navbar/', navbar_view, name='navbar'),
    path('demo/', demo, name='demo'),
    path('bill-data/', bill_data, name='bill_data'),
    path('dashboard/', dashboard_view, name='dashboard'),  # Assuming you want to render the same view
    path('stock-data/', stock_view, name='stock-data'),  # Assuming you want to render the same view
    path('item_tables_view/', item_tables_view, name='item_tables_view'),  # Assuming you want to render the same view
    path('print-bill/<int:bill_id>/', print_bill, name='print_bill'),
    path('get-items/<int:category_id>/', get_items, name='get_items')
    
]

urlpatterns  += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)