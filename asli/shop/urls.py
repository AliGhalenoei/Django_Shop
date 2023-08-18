from django.urls import path
from rest_framework import routers
from .import views

urlpatterns = [
    path('home/',views.HomeView.as_view(),name='home'),
    path('filter_category_nav/<slug:slug>/',views.HomeView.as_view(),name='filter_nav'),
    path('filter_category/<slug:slug>/',views.Filter_Category_Img.as_view(),name='filter_category'),
    path('call_me/',views.Call_Me.as_view(),name='call_me'),
    #Detail products...
    path('detail_product/<slug:slug>/',views.DetailProductView.as_view(),name='detail_product'),
    # cart...
    path('cart/',views.CartView.as_view(),name='cart'),
    path('add_cart/<int:pk>/',views.Add_Cart_View.as_view(),name='add_cart'),
    path('delete_cart/<int:pk>/',views.Delete_In_Cart_View.as_view(),name='delete_cart'),
    path('create_checkout/',views.CreateCheckoutView.as_view(),name='create_checkout'),
    path('detail_checkout/<int:pk>/',views.DetailCheckoutView.as_view(),name='detail_checkout'),
    path('cupon/<int:pk>/',views.CuponView.as_view(),name='cupon'),
    # url_list products...
    path('list_product/',views.List_Product_View.as_view(),name='list_product'),
    path('list_laptop_product/',views.List_Laptop_product_View.as_view(),name='list_laptop_product'),
    path('list_mobail_product/',views.List_Mobail_product_View.as_view(),name='list_mobail_product'),
    path('search_product/',views.Search_ProductView.as_view(),name='search_product'),
    # Api urls...
    path('list_category_api/',views.ListCategoryAPIView.as_view(),name='list_category_api'),
    path('retrieve_category_api/<slug:slug>/',views.RetrieveCategoryAPIView.as_view(),name='retrieve_category_api'),
    path('create_category_api/',views.CreateCategoryAPIView.as_view(),name='create_category_api'),
    path('update_category_api/<slug:slug>/',views.UpdateCategoryAPIView.as_view(),name='update_category_api'),
    path('Destroy_category_api/<slug:slug>/',views.DestroyCategoryAPIView.as_view(),name='Destroy_category_api'),
    
]
router=routers.SimpleRouter()
router.register('product_api_viewset',views.ProductApiViewset)
urlpatterns += router.urls
