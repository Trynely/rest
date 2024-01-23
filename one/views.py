from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from .serializers import CartSerializer, CategorySerializer, ThingsSerializer, WishlistSerializer, ImagesSerializer, PurchasesSerializer, AddPurchaseSerializer
from .models import Images, Purchases, Things, Category, Cart, Wishlist
from rest_framework.views import APIView
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

#кэш
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

#--------------------------------------------------------------------

def home(request):
    things = Things.objects.all()
    context = {
        'things': things
    }
    return render(request, 'home.html', context)


# CATEGORY

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
    


@cache_page(60 * 5)
@api_view(['GET'])
@permission_classes([AllowAny])
def CategoryThings(request, slug):
    if request.method == "GET":
        category = get_object_or_404(Category, slug=slug)
        thing = Things.objects.filter(category=category)
        serializer = ThingsSerializer(thing, many=True, context={'request': request})
        return Response(serializer.data)
    
@cache_page(60 * 5)
@api_view(["GET"])
@permission_classes([AllowAny])
def ThingImages(request):
    if request.method == "GET":
        imgs = Images.objects.all()
        serializer = ImagesSerializer(imgs, many=True, context={'request': request})
        return Response(serializer.data)

@cache_page(60 * 5)
@api_view(["GET"])
@permission_classes([AllowAny])
def ThingImagesDetail(request, pk):
    if request.method == "GET":
        thing = get_object_or_404(Things, pk=pk)
        img = Images.objects.filter(thing=thing)
        serializer = ImagesSerializer(img, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

# -----------------------------------------------------------
# THINGS

class ThingsView(generics.ListCreateAPIView):
    queryset = Things.objects.all()
    serializer_class = ThingsSerializer
    permission_classes = (AllowAny,)

    # ----------------------
    # ДЛЯ ПОЛЬЗОВАТЕЛЯ

    # def get_queryset(self):
    #     user = self.request.user
    #     return Things.objects.filter(user=user)

class ThingsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Things.objects.all()
    serializer_class = ThingsSerializer
    permission_classes = (AllowAny,)

#-------------------------------------------------------------
#FILTER AND SEACRHING THINGS

@api_view(['GET'])
@permission_classes([AllowAny])
def FilterMinThings(request, slug):
    if request.method == "GET":
        category = get_object_or_404(Category, slug=slug)
        things = Things.objects.filter(category=category).order_by("price")
        serializer = ThingsSerializer(things, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def FilterMaxThings(request, slug):
    if request.method == "GET":
        category = get_object_or_404(Category, slug=slug)
        things = Things.objects.filter(category=category).order_by("-price")
        serializer = ThingsSerializer(things, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def SearchThings(request, slug):
    if request.method == "POST":
        category = get_object_or_404(Category, slug=slug)
        search = request.data
        things = Things.objects.filter(category=category, title__icontains=search["title"])
        serializer = ThingsSerializer(things, many=True, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

#-------------------------------------------------------------
#CART

class CartView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def addToCart(request, pk):
    thing = get_object_or_404(Things, pk=pk)
    cart = Cart.objects.filter(user=request.user, title=thing.title, text=thing.text)

    if request.method == 'GET':
        if not cart.exists():
            Cart.objects.create(user=request.user, title=thing.title, text=thing.text, price=thing.price, quantity=thing.quantity, img=thing.one_img)
            print(request.user)
            print(cart.first())
        else:
            same_thing = cart.first()
            same_thing.quantity += 1
            same_thing.save()

    return JsonResponse('adding is done', safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def increaseThingCart(request, pk):
    thing = get_object_or_404(Cart, pk=pk)

    if request.method == "GET":
        thing.quantity += 1
        thing.save()

    return JsonResponse('increasing is done', safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def decreaseThingCart(request, pk):
    thing = get_object_or_404(Cart, pk=pk)

    if request.method == "GET":
        thing.quantity -= 1
        thing.save()

        if thing.quantity == 0:
            thing.delete()

    return JsonResponse('increasing is done', safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deleteFromCart(request, pk):
    cart_thing = get_object_or_404(Cart, pk=pk, user=request.user)

    if request.method == 'GET':
        cart_thing.delete()
        print(request.user)

    return JsonResponse('deleting is done', safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def clearCart(request):
    if request.method == 'GET':
        Cart.objects.filter(user=request.user).delete()
        print(request.user)

    return JsonResponse('clearning is done', safe=False)

#-------------------------------------------------------------
#WISHLIST

class WishlistView(generics.ListAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Wishlist.objects.filter(user=user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def addToWishlist(request, pk):
    thing = get_object_or_404(Things, pk=pk)
    wishlist = Wishlist.objects.filter(user=request.user, title=thing.title, text=thing.text)

    if request.method == 'GET':
        if not wishlist.exists():
            Wishlist.objects.create(user=request.user, title=thing.title, text=thing.text, price=thing.price, quantity=thing.quantity, img=thing.one_img)
            print(request.user)
            print(wishlist.first())
        else:
            same_thing = wishlist.first()
            same_thing.quantity += 1
            same_thing.save()

    return JsonResponse('adding is done', safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deleteFromWishlist(request, pk):
    wishlist_thing = get_object_or_404(Wishlist, pk=pk, user=request.user)

    if request.method == 'GET':
        wishlist_thing.delete()
        print(request.user)

    return JsonResponse('deleting is done', safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def clearWishlist(request):
    if request.method == 'GET':
        Wishlist.objects.filter(user=request.user).delete()
        print(request.user)

    return JsonResponse('clearning is done', safe=False)


# -----------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def purchases(request):
    if request.method == "GET":
        purchases = Purchases.objects.all()
        serializer = PurchasesSerializer(purchases, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def addPurchase(request):
    if request.method == "POST":
        serializer = AddPurchaseSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data)

            return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)