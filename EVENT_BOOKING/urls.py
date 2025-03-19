"""
URL configuration for EVENT_BOOKING_PROJECT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from.import views
from django.conf import settings
from django.conf.urls.static import static
from.views import delete_package
from .views import owner_home



urlpatterns = [
    path('',views.index,name='index'),
    path('index/',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('home/',views.new,name='home'),
    path('userlist/',views.userlist,name='userlist'),
    path('deleteuser/<int:id>',views.deleteuser,name='deleteuser'),
    path('profile/',views.userprofile,name='profile'),
    # path('selection/',views.selection,name='selection'),
    # path('selectionlist/',views.selectionlist,name='selectionlist'),
    # path('deleteselection/<int:id>',views.deleteselection,name='deleteselection'),
    path('update_profile/',views.update_profile,name='update_profile'),
    path('update_pro/',views.update_pro,name='update_pro'),
    path('adminhome/',views.adminhome,name='adminhome'),
    path('feedback_rate/',views.feedback_view,name='feedback_rate'),
    path('feedback_success/',views.feedback_success,name='feedback_success'),
    path('feedbacklist/',views.feedbacklist,name='feedbacklist'),
    path('deletefeedback/<int:id>',views.deletefeedback,name='deletefeedback'),
    path('user_cart/', views.user_cart, name='user_cart'),
    path('carts/', views.decorcart, name='carts'),
    path('dcarts/', views.dcarts, name='dcarts'),
    path('buy_decoration/<int:decoration_id>/', views.buy_decoration, name='buy_decoration'),
    path('decoration_payment_success/<int:cart_id>/', views.decoration_payment_success, name='decoration_payment_success'),
    # path('book/<int:decoration_id>/', views.book_decoration, name='book_decoration'),
    path('book_decoration/<int:decoration_id>/', views.book_decoration, name='book_decoration'),
    path('Owner_login/',views.Owner_login,name='Owner_login'),
    path('Owner_list/',views.Owner_list,name='Owner_list'), 
    path('deleteowner/<int:id>',views.deleteowner,name='deleteowner'),
    path('Owner_register/',views.Owner_register,name='Owner_register'),
    path('admin_dashboard/',views.admin_dash,name='admin_dashboard'),
    path('category/',views.category,name='category'),
    path('update_status/',views.update_status,name='update_status'),
    path('logout/',views.logout,name='logout'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('owner_profile/',views.owner_profile,name='owner_profile'),
    path('chef_login/',views.cheflogin,name='chef_login'),
    path('chef_profile/',views.chefprofile,name='chef_profile'),
    path('chef_register/',views.chefregister,name='chef_register'),
    path('chefdb/',views.chefdatabase,name='chefdb'),
    path('deletechefuser/<int:id>',views.deletechefuser,name='deletechefuser'),
    path('chefhome/',views.chefpage,name='chefhome'),
    path('chef_status/',views.chef_status,name='chef_status'),
    path('chef_update/',views.chefupdate_pro,name='chef_update'),
    path('chefrecipe/',views.Chefrecipe,name='chefrecipe'),
    path('viewrecipe/',views.viewrecipe,name='viewrecipe'),
    path('chefupdate_pro/',views.chefupdate_pro,name='chefupdate_pro'),
    path('organizereventcreate/',views.addevents,name='organizereventcreate'),
    path('chefcard/',views.list,name='chefcard'),
    path('chat_detail/',views.chat_detail,name='chat_detail'),
    path('chat_list/',views.chat_list,name='chat_list'),
    path('chefbookingform/<int:chef_id>/',views.chefbookingform,name='chefbookingform'),
    path('user_transactions/', views.user_transactions, name='user_transactions'),
    path('utidectransactions/', views.utidectransactions, name='utidectransactions'),
    path('cheftransactions/', views.cheftransactions, name='cheftransactions'),


    path('add_cart/<int:pid>/',views.add_cart,name='add_cart'),
    path('cart_list/',views.cart_list,name='cart_list'),
    path('initiate-payment/<id>/', views.initiate_payment, name='initiate-payment'),
    path('confirm-payment/<order_id>/<payment_id>/<crti_id>/', views.confirm_payment, name='confirm-payment'),


    path('chef_carts/', views.chef_carts, name='chef_carts'),
    # path('chef_cart_detail/<int:pk>/', chef_cart_detail, name='chef_cart_detail'),
    path('utensils/', views.utensils, name='utensils'),
    # path('decoration/', views.decoration, name='decoration'),
    path('utensils_list/',views.utensils_list,name='utensils_list'),
    # path('decoration_list/',views.decoration_list,name='decoration_list'),
    path('create_order/', views.create_order, name='create_order'),
    path("save_payment/", views.save_payment, name="save_payment"),
    # path('create_orderd/', views.create_orderd, name='create_orderd'),
    # path("save_paymentd/", views.save_paymentd, name="save_paymentd"),
    path("myutensilslist/", views.myutensilslist, name="myutensilslist"),
    path('mytransutensilslist/', views.mytransutensilslist, name='mytransutensilslist'),
    path('edit_utensils/<int:utensil_id>/', views.edit_utensils, name='edit_utensils'),
    path('delete_utensils/<int:utensil_id>/', views.delete_utensils, name='delete_utensils'),
    path('request_refund/', views.request_refund, name='request_refund'),
    path('ref/', views.refreq, name='refreq'),
    path('approve_refund/<int:refund_id>/', views.approve_refund, name='approve_refund'),
    path('payment/<str:payment_id>/', views.payment_page, name='payment_page'),  # Add this view to show the payment page
    path('payment/success/<str:order_id>/<str:payment_id>/', views.payment_success, name='payment_success'),
    path('reject-refund/<int:refund_id>/', views.reject_refund, name='reject_refund'),
    path('payment/success/<str:order_id>/<str:payment_id>/', views.payment_success, name='payment_success'),
    path('decorations/<int:pk>/', views.decoration_detail, name='decoration_detail'),
    path('buy_all_decorations/', views.buy_all_decorations, name='buy_all_decorations'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_failed/', views.payment_failed, name='payment_failed'),




    # path('decorations/', views.decorations_list, name='decorations_list'),
    # path('decorations/add/', views.add_decoration, name='add_decoration'),
    # path('decorations/edit/<int:id>/', views.edit_decoration, name='edit_decoration'),





    path('createdecorations/', views.createdecoration, name='createdecoration'),
    path('chat/', views.chat_list, name='chat_list'),
    path('chat_detail/<str:user_type>/<str:username>/', views.chat_detail, name='chat_detail'),
    path('chat/delete_message/<int:message_id>/', views.delete_message, name='delete_message'),


    path('decorations/edit/<int:id>/', views.edit_decoration, name='edit_decoration'),
    path('declist/', views.declist, name='declist'),
    path('declist/update/<int:id>/', views.update_decoration, name='update_decoration'),
    path('decorations/delete/<int:id>/', views.delete_decoration, name='delete_decoration'),

    path('chef_events/',views.chef_events, name='chef_events'),
    path('delete-package/<int:package_id>/', delete_package, name='delete_package'),
    path('decorsview/', views.decorsview, name='decorsview'),

  



    path('Ownerhome/', owner_home, name='owner_home'),

    path('list_utensils/', views.list_utensils, name='list_utensils'),
    

  

    

    
]
#if settings.DEBUG:
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    