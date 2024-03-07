from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser,FileUploadParser
from rest_framework import viewsets,status,generics,mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .serializers import *
from authentication.serializers import CustomUserSerializer,ConsumerSerializer,AddressSerializer

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view,parser_classes,action

from django.contrib import messages
# Create your views here.
from .forms import *

from datetime import date
from django.contrib.auth.decorators import login_required

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class=CategorySerializer
    parser_class=(FormParser)
    queryset=Category.objects.all()

class SubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class=SubCategorySerializer
    parser_class=(FormParser)
    queryset=SubCategory.objects.all()
    
    def create(self,request):
        subcat_serializer=SubCategorySerializer(data=request.data)
        subcat_serializer.is_valid(raise_exception=True)
        subcat_instance=subcat_serializer.save()
        
        response_data={
            'sub_category' : {
                'id': subcat_instance.id,
                'category_id':subcat_instance.id,
                'title': subcat_instance.title,
                'details': subcat_instance.details,
            },
        }
        
        headers=self.get_success_headers(subcat_serializer.data)
        return Response(response_data,status=status.HTTP_201_CREATED,headers=headers)
    
class SubCategoryList(viewsets.ModelViewSet):
    def retrieve(self,request,pk):
        queryset=SubCategory.objects.all()
        if request.method=='GET':
            subcategory=get_object_or_404(queryset,pk=pk)
            serializer=SubCategorySerializer(subcategory)
            category_id=serializer.data['category']
            category=Category.objects.get(id=category_id)
            cat_serializer=CategorySerializer(category)
            
            return Response({'sub_category':serializer.data,'category':cat_serializer.data})

         
class ManufacturerViewSet(viewsets.ModelViewSet):
    serializer_class=ManufacturerSerializer
    parser_class=(FormParser)
    queryset=Manufacturer.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class=ProductSerializer
    parser_class=(FormParser)
    queryset=Product.objects.all()
    
class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class=PhotoSerializer
    queryset=Photo.objects.all()
    parser_classes=(MultiPartParser,FormParser)
    
class OfferViewSet(viewsets.ModelViewSet):
    serializer_class=OfferSerializer
    queryset=Offer.objects.all()
    parser_class=(FormParser)
    
class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class=FeedbackSerializer
    queryset=Feedback.objects.all()
    parser_class=(FormParser)
    
class ProductDetails(viewsets.ModelViewSet):
    def retrieve(self,request,pk):
        if request.method=='GET':
            prod_set=Product.objects.all()
            products=get_object_or_404(prod_set,pk=pk)
            prod_serializer=ProductSerializer(products)
            print('products',products)
            
            offer_set=Offer.objects.get(product=products)
            offer_serializer=OfferSerializer(offer_set)
            
            photo_set=Photo.objects.get(product=products)
            photo_serializer=PhotoSerializer(photo_set)
            return Response({
                'product':prod_serializer.data,
                'offer':offer_serializer.data,
                'photo':photo_serializer.data,
            })

class ProductPhotoDetails2(viewsets.ModelViewSet):
    serializer_class=ProductDetailsSerializer
    queryset=Product.objects.all()
    parser_class=(MultiPartParser)
    
    
class ProductPhotoDetails(generics.CreateAPIView):
    serializer_class=ProductPhotoSerializer
    parser_class=(MultiPartParser)
    def create(self,request):
        if request.method=="POST":
            serializer=ProductSerializer(data=request.data)
            print("serializer Data",serializer)
            if serializer.is_valid():
                print("Post Data",request.FILES.getlist('uploaded_images'))
                uploaded_images=request.FILES.getlist('uploaded_images')
                product_instance=serializer.save()
                
                print('product_data',product_instance)
                
                for image in uploaded_images:
                    Photo.objects.create(product=product_instance,files=image)
                
                return Response({'product':serializer.data},status=status.HTTP_201_CREATED)
                
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class AddressViewSet(viewsets.ModelViewSet):
    # permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    serializer_class=AddressSerializer
    queryset=Address.objects.all()
    parser_class=(FormParser)

class ViewCartDetails(viewsets.ViewSet):
    def list(self,request):
        queryset=Order.objects.filter(status='Cart')
        serializer=CartSerializer(queryset,many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class=OrderSerializer
    queryset=Order.objects.filter(status='Order Placed')
    parser_class=(FormParser)








def homepage(request):
    
    prod_set=Product.objects.all()
    man_set=Manufacturer.objects.all()
    cat_set=Category.objects.all()
    subcat_set=SubCategory.objects.all()
    photo_set=Photo.objects.all()
    
    context={
            'products_list':prod_set,
            'manufacturer':man_set,
            'category':cat_set,
            'subcategory':subcat_set,
            'photo':photo_set,
            }
        
    if request.method=='POST':
        man_id=request.POST.getlist('man_id')
        subcat_id=request.POST.getlist('subcat_id')
        price_range=request.POST.get('price_range')
        
        print('Form Data:',request.POST,'/n')
        print('Sub_Cats:',subcat_id,'/n')
        print('Mans:',man_id,'/n')
        
        query=Q()
        
        if subcat_id:
            query &= Q(subcategory__id__in=subcat_id)
        if man_id:
            query &= Q(manufacturer__id__in=man_id)
        if price_range:
            query &= Q(price__gte=price_range) 
        
        prod_list=Product.objects.filter(query)
        
        context={
            'filtered_products_list':prod_list,
            'photo':photo_set,
            'manufacturer':man_set,
            'category':cat_set,
            'subcategory':subcat_set,
        }
        return render(request,'home.html',context)
    
    return render(request,'home.html',context)

    
def view_product_by_category(request,subcat_id):
    prod_set=Product.objects.filter(subcategory=subcat_id)
    prod_serializer=ProductDetailsSerializer(prod_set,many=True)
    
    cat_set=Category.objects.all()
    cat_serializer=CategorySerializer(cat_set,many=True)
    
    subcat_set=SubCategory.objects.all()
    subcat_serializer=SubCategorySerializer(subcat_set,many=True)
    
    context={
        'category':cat_serializer.data,
        'subcategory':subcat_serializer.data,
        'products':prod_serializer.data,
    }
    return render(request,'products_sorted.html',context)


def view_product(request,cat_id):
    if request.user.id is not None:
        prod_set=Product.objects.get(id=cat_id)
        prod_serializer=ProductDetailsSerializer(prod_set)
        user_set=Consumer.objects.get(consumer_admin=request.user)
        user_serializer=ConsumerSerializer(user_set)
        print("Product Details", prod_serializer.data)
        context={
            'product':prod_serializer.data,
            'user_details':user_serializer.data,
            }
        return render(request,'products.html',context)
    else:
        prod_set=Product.objects.get(id=cat_id)
        prod_serializer=ProductDetailsSerializer(prod_set)
        context={
            'product':prod_serializer.data,
            }
        return render(request,'products.html',context)
        


def add_to_cart(request):
    if request.user is not None:
        user=Consumer.objects.get(consumer_admin=request.user)
        if request.method=="POST":
            product_id=request.POST.get('product_id')
            prod_set=Product.objects.get(id=product_id)
            quantity=request.POST.get('quantity')
            product_amount=prod_set.price
            cart_price=product_amount * float(quantity)
            order=Order.objects.create(
                user=user,
                product=prod_set,
                quantity=quantity,
                total_amount=cart_price,
                status='Cart'
            )
            messages.success(request,"Item Added to Cart Successfully")
            return redirect('view_cart')
        return render(request,'cart.html')

def view_cart(request):
    if request.user:
        consumer=Consumer.objects.get(consumer_admin=request.user)
        order_set=Order.objects.filter(user=consumer,status='Cart')
        serializer=CartSerializer(order_set,many=True)
        
        address_set=Address.objects.filter(user=consumer)
        address_serializer=AddressSerializer(address_set,many=True)
        
        cart_total=0.0
        for i in serializer.data:
            cart_total+=i.get('total_amount')
        gst_amount=(cart_total * 18)/100
        final_price=cart_total+gst_amount
        context={
            'cart_data':serializer.data,
            'cart_total':cart_total,
            'gst_amount':gst_amount,
            'final_price':final_price,
            'address':address_serializer.data,
        }
       
        
        return render(request,'cart.html',context)

def confirm_order(request):
    if request.method=="POST":
        address_id=request.POST.get('address_id')
        address=Address.objects.get(id=address_id)
        orders=request.POST.getlist('orders[]')
        print("Products",orders)
        print("address_id",address_id)
        for i in orders:
            order=Order.objects.get(id=i)
            order.delivery_address=address
            order.status='Order Placed'
            order.save()
        messages.success(request,"Order Has Been Placed Succssfully")
        return redirect('view_history')

def view_history(request):
    consumer=Consumer.objects.get(consumer_admin=request.user)
    order=Order.objects.filter(user=consumer,status='Order Placed')
    serializer=OrderSerializer(order,many=True)
    serializer.data[0]
    print("current date",serializer.data[0]['date_added'])
    

    context={
        'history':serializer.data,
    }
    return render(request,'history.html',context)

def remove_cart(request,order_id):
    order=Order.objects.get(id=order_id)
    print("order",order)
    order.delete()
    messages.success(request,"Item has been removed from cart")
    return redirect('view_cart')

@login_required(login_url ='login_page')
def feedback(request):
    if request.method=="POST":
        print("Form Data", request.data)
        return redirect('feedback')
    context={
        'form':FeedBackConsumerForm,
    }
    return render(request,'feedback.html',context)
 


                
        