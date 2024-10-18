"""
URL configuration for mysite project.

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
from myapp import views
from django.urls import re_path as url
urlpatterns = [
    path("admin/", admin.site.urls),
    # path("hello/", views.hello,name='hello'),
    path("initialise/", views.initialise,name='initialise'),
    path("Taiwan_movies_all/", views.Taiwan_movies_all,name='Taiwan_movies_all'),
    path("Taiwan_movies_all/shop/", views.shop,name='shop'),
    path('shop/', views.shop, name='shop'),  # 商店頁
    path('product-details/', views.product_details, name='product_details'),  # 產品詳情頁
    path('contact/', views.contact, name='contact'),  # 聯繫我們頁
    path('signin/', views.hello, name='hello'),  # 登錄頁
    path('check_email/', views.check_email, name='check_email'),
    path('Taiwan_movies_all/Line', views.Line, name='Line'),
    path('Taiwan_movies_all/user_more', views.user_more, name='user_more'),
    path('Taiwan_movies_all/handle/', views.handle, name='handle'),
    path('Taiwan_movies_all/favorite_page/', views.favorite_page, name='favorite_page'),
    path('Taiwan_movies_all/about_us/', views.about_us, name='about_us')
]
