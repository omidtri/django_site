from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list_page'),
    path('comment/add-product-comment', views.add_product_comment, name='add_product_comment'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('cat/<cat>', views.ProductListView.as_view(), name='product-categories-list'),
    path('brand/<brand>', views.ProductListView.as_view(), name='product-list-by-brands'),
    path('search/', views.searcher, name='search_page')
]
