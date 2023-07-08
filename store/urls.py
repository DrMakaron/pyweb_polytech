from django.urls import path

from rest_framework import routers

from store.views import SingleProductView, CartView, ShopView, CartViewSet, WishListView, add_to_wishlist, \
    remove_from_wishlist, WishViewSet

router = routers.DefaultRouter()
router.register(r'cart', CartViewSet)

wish_router = routers.DefaultRouter()
wish_router.register(r'wishlist', WishViewSet)

app_name = 'store'

urlpatterns = [
    path('product/<int:id_>', SingleProductView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    path('', ShopView.as_view(), name='shop'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('wishlist', WishListView.as_view(), name='wishlist'),
    path('wishlist/add<int:id_>', add_to_wishlist),
    path('wishlist/remove<int:id_>', remove_from_wishlist)

]
