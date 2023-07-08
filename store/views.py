from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db.models import Case, When, DecimalField, F, ExpressionWrapper

from rest_framework import viewsets, response
from rest_framework.permissions import IsAuthenticated

from .serializers import CartSerializer

from store.models import Product, Cart, WishList


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        cart_items = self.get_queryset().filter(product__id=request.data.get('product'))
        if cart_items:
            cart_item = cart_items[0]
            if request.data.get('quantity'):
                cart_item.quantity += int(request.data.get('quantity'))
            else:
                cart_item.quantity += 1
        else:
            product = get_object_or_404(Product, id=request.data.get('product'))
            if request.data.get('quantity'):
                cart_item = Cart(user=request.user, product=product, quantity=request.data.get('quantity'))
            else:
                cart_item = Cart(user=request.user, product=product)

        cart_item.save()

        return response.Response({'message': 'Product added to cart'})

    def update(self, request, *args, **kwargs):
        cart_item = get_object_or_404(Cart, id=kwargs['pk'])
        if request.data.get('quantity'):
            cart_item.quantity = request.data['quantity']
        if request.data.get('product'):
            product = get_object_or_404(Product, id=request.data['product'])
            cart_item.product = product
        cart_item.save()
        return response.Response({'message': 'Product changed in cart'})

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_queryset().get(id=kwargs['pk'])
        cart_item.delete()
        return response.Response({'message': 'Cart item deleted'})


# Create your views here.
class SingleProductView(View):
    @staticmethod
    def get(request, id_):
        data = Product.objects.get(id=id_)
        return render(request, 'product-single.html', context={'data': data})


class CartView(View):
    @staticmethod
    def get(request):
        return render(request, 'cart.html')


class ShopView(View):
    @staticmethod
    def get(request):
        discount_value = Case(When(discount__value__gte=0,
                                   then=F('discount__value')),
                              default=0,
                              output_field=DecimalField(max_digits=10, decimal_places=2)
                              )

        price_with_discount = ExpressionWrapper(
            F('price') * (100.0 - F('discount_value')) / 100.0,
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )

        products = Product.objects.annotate(
            discount_value=discount_value,
            price_before=F('price'),
            price_after=price_with_discount
        ).values('id', 'name', 'image', 'price_before', 'price_after',
                 'discount_value')

        return render(request, 'shop.html', context={'data': products})


class WishListView(View):

    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            user_wishes = WishList.objects.filter(user_id=request.user.id)
            print(user_wishes.values('product_id'))
            products = Product.objects.filter(id__in=user_wishes.values('product_id'))
            return render(request, 'wishlist.html', context={'data': products})
        else:
            return redirect('login')


def add_to_wishlist(request, id_):
    if not WishList.objects.filter(user_id=request.user.id).filter(product_id=id_):
        WishList.objects.create(product_id=id_, user_id=request.user.id)

    return redirect('/shop')
