from django.contrib import admin
from django.urls import path

from .forms import CreateMenuItem
from .views import *

app_name = 'cafe5'

urlpatterns = [
    path('orders/', orders_list, name='all_orders'),
    path('add_order/', add_order, name='add_order'),
    path('order/<int:order_num>', order_details, name='order_details'),
    path('add_new_order', AddOrderView.as_view(), name='add_new_order_by_class_view'),
    path('orders_list/', OrderList.as_view(), name='orders_list_by_class_view'),
    path('o/<int:number>', OrderDetails.as_view(), name='order_details_by_class_view'),
    path('allorders/', AllOrders.as_view(), name='all_orders_generic_view'),
    path('<int:pk>', OrderDetails2.as_view(), name='order_details_generic_view'),
    path('addneworder/', AddNewOrder.as_view(), name='add_new_order_generic_view'),
    path('CreateMenuItem/', form_test.as_view(), name='CreateMenuItem'),

]
