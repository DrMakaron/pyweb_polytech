from django.urls import path

from rest_framework import routers

from store.views import SingleProductView, CartView, ShopView, CartViewSet, WishListView

router = routers.DefaultRouter()
router.register(r'cart', CartViewSet)

app_name = 'store'

urlpatterns = [
    path('product/<int:id_>', SingleProductView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    path('', ShopView.as_view(), name='shop'),
    path('wishlist', WishListView.as_view(), name='wishlist')
]
