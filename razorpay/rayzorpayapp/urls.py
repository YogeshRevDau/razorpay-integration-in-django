from django.urls import path
from . import views

urlpatterns = [
    path('',views.OrderView,name='create_order'),
    path('pay/<str:order_id>',views.paymentView,name='payment'),
    path('success',views.successView,name='success'),
    path('show',views.showView,name='show'),
    path('refund/<str:order_id>/', views.initiate_refund, name='initiate_refund'),
]