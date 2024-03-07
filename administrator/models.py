from django.db import models
from authentication.models import Consumer
# Create your models here.

class Category(models.Model):
    title=models.CharField(max_length=50)
    details=models.TextField()
    
    def __str__(self):
        return str(self.title)

class Manufacturer(models.Model):
    name=models.CharField(max_length=50)
    origin=models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.name) + str(self.origin)

    
class SubCategory(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    details=models.TextField()
    
    def __str__(self):
        return str(self.category.title) + str(self.title)
    
class Product(models.Model):
    subcategory=models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    manufacturer=models.ForeignKey(Manufacturer,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    price=models.FloatField()
    description=models.TextField()
    warranty=models.CharField(max_length=50)
    date_added=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50)
    quantity=models.IntegerField()
    
    def __str__(self):
        return str(self.title) + str(self.subcategory.title)

class Photo(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='photo')
    files=models.ImageField(upload_to='file_uploads/')
    
    def __str__(self):
        return str(self.product) + str(self.path)
    

class Offer(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    discount=models.FloatField()
    start_date=models.DateField()
    end_date=models.DateField()
    description=models.TextField()
    
    def __str__(self):
        return str(self.product.title) + str(self.title)

class Address(models.Model):
    user=models.ForeignKey(Consumer,on_delete=models.CASCADE,related_name='address')
    title=models.CharField(max_length=50)
    landmark=models.CharField(max_length=50)
    pincode=models.IntegerField()
    type=models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.title) +" "+ str(self.user.consumer_admin.first_name)
    
class Faq(models.Model):
    user=models.ForeignKey(Consumer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    query=models.TextField()
    reply=models.TextField(null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user.consumer_admin.first_name) +" "+ str(self.query)

class Feedback(models.Model):
    user=models.ForeignKey(Consumer,on_delete=models.CASCADE)
    content=models.TextField()
    reply=models.TextField(null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user.cosumer_admin.first_name)+" "+str(self.content)
  
class Payment(models.Model):  
    type=models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.type)
    
    
class Order(models.Model):
    user=models.ForeignKey(Consumer,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    delivery_address=models.ForeignKey(Address,on_delete=models.CASCADE,null=True)
    date_added=models.DateField(auto_now_add=True)
    quantity=models.IntegerField(null = True)
    total_amount=models.FloatField(null=True)
    status=models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.user.consumer_admin.first_name)+" "+str(self.product.title)


class History(models.Model):
    user_id=models.IntegerField()
    product=models.CharField(max_length=50)
    payment=models.CharField(max_length=50)
    paid_amount=models.FloatField()
    order_placed=models.DateTimeField()
    delivery_address=models.TextField()