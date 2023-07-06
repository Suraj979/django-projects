from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Wishlist, Cart
from .serializers import ProductSerializer
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import User

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Additional fields can be extracted from the request
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_to_wishlist(request):
    user = request.user
    product_id = request.data.get('product_id')
    product = Product.objects.get(id=product_id)
    wishlist = Wishlist(user=user, product=product)
    wishlist.save()
    return Response('Added to wishlist')



