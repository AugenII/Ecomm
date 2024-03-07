from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,parser_classes,action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView,TokenVerifyView
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework import generics,status,viewsets
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.contrib import messages
# Create your views here.
from . models import *
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from .tokens import create_jwt_pair_for_user
from .forms import *
from verify_email.email_handler import send_verification_email

from django.core.mail import send_mail
import datetime

UserModel=get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer  
    
class MyTokenVerifyView(TokenVerifyView):
    pass

class UserRegistration(generics.CreateAPIView):
    serializer_class=RegisterSerializer
    parser_class=(FormParser)
    
    def create(self,request):
        if request.method=="POST":
            serializer=RegisterSerializer(data=request.data)
            if serializer.is_valid():
                first_name=serializer.data['first_name']
                last_name=serializer.data['last_name']
                username=serializer.data['username']
                email=serializer.data['email']
                password=serializer.data['password']
                
                customuser=CustomUser.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                )
                customuser.set_password(password)
                customuser.user_type=2
                customuser.save()
                
                phone_no = serializer.data['phone_no']
                
                consumer=Consumer.objects.create(
                    consumer_admin=customuser,
                    phone_no=phone_no,
                )
                
                return Response({'CustomUser':serializer.data},status=status.HTTP_201_CREATED)
            else:
                return Response({'CustomUser':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class ViewUsers(viewsets.ModelViewSet):
    serializer_class=ConsumerSerializer
    queryset=Consumer.objects.all()
    
    
class LoginView(generics.CreateAPIView):
    permission_classes=[]
    serializer_class=LoginSerializer
    def post(self,request):
        email=request.data.get("email")
        password=request.data.get("password")
        user=authenticate(email=email,password=password)
        
        if user is not None:
            tokens=create_jwt_pair_for_user(user)
            response={"message":"Login Successful","tokens":tokens}
            return Response(data=response,status=status.HTTP_200_OK)
        
        else:
            return Response(data={"message":"invalid email or password"},status=status.HTTP_404_NOT_FOUND)

def register(request):
    cuform=CustomUserInputForm(request.POST, request.FILES)
    if request.method == "POST":
        if cuform.is_valid():
            email=cuform.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email).exists():
                messages.warning(request, 'email is already taken')
                return redirect('add_airline_email_test')
            else:
                password=cuform.cleaned_data.get('password')
                user_form=cuform.save(commit=False)
                user_form.set_password(password)
                user_form.user_type='2'
                user_data=send_verification_email(request,cuform)
                
                phone = request.POST.get('phone_no')
                consumer = Consumer(
                    consumer_admin=user_data,
                    phone_no=phone,
                )
                consumer.save()
                return redirect('login_page')
    else:
        cuform=CustomUserInputForm()

    context={
        'custom_user_form':cuform,
    }
    return render(request,'register.html',context)
        
        
def dologin(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user=UserModel.objects.get(email=email)
            print("try block user:",user)
            if user.check_password(password):
                print("password verified")
                user=authenticate(email=email,password=password)
                print("auth begins:",user)
                if user is not None:
                    try:
                        if user.user_type=='1':
                            login(request,user)
                            return redirect('admin')
                        elif user.user_type=='2':
                            if user.is_active == True:
                                print("current user",user)
                                login(request,user)
                                messages.success(request,"Login Successful")
                                return redirect('home')
                            else:
                                messages.error(request,"Please actiate your acoount")
                                return redirect('login_page')
                        else:
                            messages.error(request,"Inavlid user details")
                            return redirect('login_page')
                    except:
                        pass
                else:
                    messages.error(request,"No user accounts found")
                    return redirect('login_page')
            else:
                messages.error(request,'Invalid Password')
                return redirect('login_page')
        except UserModel.DoesNotExist:
            messages.error(request,'No User Found')
            return redirect('login_page')
    return render(request, 'login.html')

def check_mail(request):
    check_mail=request.POST.get('email2')
    user=UserModel.objects.get(email=check_mail)
    context={
        'user_data':user
    }
    if user is not None:
        return render(request,'forgot_password.html',context)
    else:
        messages.info(request,"sorry invalid mail id")
        redirect('login')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('mail')
        password = request.POST.get('password1')
        password2=request.POST.get('password2')
        
        if password != password2:
            messages.error(request,"The Passwords does not matches")
            return redirect('forgot_password')
        
        try:
            user = UserModel.objects.get(email=email)
            user.set_password(password)
            user.save()
            now = datetime.datetime.now()
            mesage=f'Your password has been changed on {now}'
            send_mail(
                "Password Reset",
                f"Your Password Hase been Changed {now}",
                from_email=None,
                recipient_list=[email],
                fail_silently=False,
            )
            print("user",user)
            messages.success(request, 'Password Reset was Successfull !')
            return redirect('login_page')
        except:
            messages.error(request,"Invalid credentials")
    return render(request, 'forgot_password.html')

def dologout(request):
    logout(request)
    return redirect('home')

# @swagger_auto_schema(request_body=CategorySerializer,methods=['post'])
# @api_view(['POST'])
# @parser_classes([FormParser])
# def example_view(request, format=None):
#     if request.method == 'POST':
#         serializer = CategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         instance = serializer.save()

#         response_data = {
#             'id':instance.id,
#             'title':instance.title,
#             'details':instance.details,
#         }
#     return Response(response_data)
        
        