from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from . models import *
from authentication.serializers import ConsumerSerializer,AddressSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'
        
class SubCategorySerializer(serializers.ModelSerializer):
    category=CategorySerializer(read_only=True)
    class Meta:
        model=SubCategory
        fields=('id','category','title','details')

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Manufacturer
        fields='__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Photo
        fields=["id","files"]
        
class ProductPhotoSerializer(serializers.ModelSerializer):
    photos=PhotoSerializer(many=True,read_only=True)
    uploaded_images=serializers.ListField(child=serializers.ImageField(allow_empty_file=False,use_url=False),write_only=True)
    class Meta:
        model=Product
        fields=["id","title","price","date_added","description","warranty","status","uploaded_images","subcategory","manufacturer","photos"]

        
class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model=Offer
        fields='__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Offer
        fields='__all__'

class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model=Faq
        fields='__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model=Feedback
        fields='__all__'

        

#multiple serializers

class ProductDetailsSerializer(serializers.ModelSerializer):
    subcategory=SubCategorySerializer(read_only=True)
    manufacturer = ManufacturerSerializer(read_only=True)
    photo=PhotoSerializer(read_only=True,many=True)
    class Meta:
        model=Product
        fields=["id","title","price","date_added","description","warranty","status","photo","quantity","subcategory","manufacturer"]


class CartSerializer(serializers.ModelSerializer):
    user=ConsumerSerializer(read_only=True)
    product=ProductDetailsSerializer(read_only=True)
    class Meta:
        model=Order
        fields=["user","status","product","id","total_amount","date_added","quantity"]
        
class OrderSerializer(serializers.ModelSerializer):
    user=ConsumerSerializer(read_only=True)
    product=ProductDetailsSerializer(read_only=True)
    delivery_address=AddressSerializer(read_only=True)
    offer=OfferSerializer(read_only=True)
    
    class Meta:
        model=Order
        fields=['user','product','offer','delivery_address','status','quantity','total_amount','date_added']