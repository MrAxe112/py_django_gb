import ordersapp.views as ordersapp
from django.urls import path

app_name = "ordersapp"

urlpatterns = [
   path('', ordersapp.OrderList.as_view(), name='list'),
   path('read/<int:pk>', ordersapp.OrderDetailView.as_view(), name='read'),
   path('create/', ordersapp.OrderCreateView.as_view(), name='create'),
   path('update/<int:pk>', ordersapp.OrderUpdateView.as_view(), name='update'),
   path('delete/<int:pk>', ordersapp.OrderDeleteView.as_view(), name='delete'),
   path('cancel/forming/<int:pk>', ordersapp.forming_complete, name='forming_complete'),
]