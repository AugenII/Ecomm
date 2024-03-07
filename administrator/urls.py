from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers
from django.shortcuts import get_object_or_404
from . import views
from . import views as admin_views

router=routers.DefaultRouter()

router.register('categories',admin_views.CategoryViewSet,basename='categories')
router.register('subcategories',admin_views.SubCategoryViewSet,basename='subcategory')
router.register('manufacturer',admin_views.ManufacturerViewSet,basename='manufacturer')
router.register('products',admin_views.ProductViewSet,basename='products')
router.register('photos',admin_views.PhotoViewSet,basename='photos')
router.register('offers',admin_views.OfferViewSet,basename='offers')
router.register('address',admin_views.AddressViewSet,basename='address')
router.register('order',admin_views.OrderViewSet,basename='oders')
router.register('feedback_viewset',admin_views.FeedbackViewSet,basename='feedback_viewset')
router.register('product_photo2',admin_views.ProductPhotoDetails2,basename='productphto')

urlpatterns=[
    
    path('',include(router.urls)),
    path('sub_categories_list/<str:pk>',admin_views.SubCategoryList.as_view({'get': 'retrieve'}),name='subcategory_list'),
    path('product_details/<str:pk>',admin_views.ProductDetails.as_view({'get':'retrieve'}), name='product_details'),
    
    path('product_photo/',admin_views.ProductPhotoDetails.as_view(),name='product_photo_upload'),
    path('view_product_by_category/<int:subcat_id>',admin_views.view_product_by_category,name='view_product_by_category'),
    path('view_product/<int:cat_id>',admin_views.view_product,name='view_product'),
    path('add_to_cart',admin_views.add_to_cart,name="add_to_cart"),
    path('view_cart',admin_views.view_cart,name='view_cart') ,
    path('remove_cart/<int:order_id>',admin_views.remove_cart, name='remove_cart'),
    path('confirm_order',admin_views.confirm_order,name="confirm_order"),
    path('view_history',admin_views.view_history,name='view_history'),
    
    path('feedback',admin_views.feedback,name='feedback'),
    
]