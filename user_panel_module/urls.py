from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserPanelDashboardView.as_view(), name='user_panel_dashboard'),
    path('change-pass/', views.ChangePasswordView.as_view(), name='change_password_page'),
    path('edit-profile/', views.EditUserProfileView.as_view(), name='edit_profile_page'),
    path('user-basket', views.user_basket, name='user_basket_page'),
    path('my-shopping', views.MyShopping.as_view(), name='user_shopping_page'),
    path('my-shopping-detail/<order_id>', views.my_shopping_detail, name='user_shopping_detail_page'),
    path('remove-order-detail', views.remove_order_detail, name='remove_order_detail_ajax'),
    path('change-order-detail', views.change_order_detail_count, name='change_order_detail_count_ajax'),
    path('warranty/', views.WarrantyView.as_view(), name='warranty_page'),
    path('discount/', views.DiscountView.as_view(), name='discount_page')

]
