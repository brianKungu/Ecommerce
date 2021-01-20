from django.urls import path
from .views import (
    ProductDetailView,
    CheckoutView,
    cart,
    StoreView,add_to_cart,remove_from_cart,OrderSummaryView,remove_single_item_from_cart,Payment
)

app_name='store'

urlpatterns=[
    path('', StoreView.as_view() ,name='store'),
    # path('cart', cart, name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='cart'),
    path('product/<slug>/',ProductDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>', add_to_cart , name='add_to_cart'),
    path('remove-from-cart/<slug>', remove_from_cart , name='remove_from_cart'),
    path('remove-item-from-cart/<slug>', remove_single_item_from_cart , name='remove_single_item_from_cart'),
    path('payment/<payment_option>', Payment.as_view(), name='payment')    
]