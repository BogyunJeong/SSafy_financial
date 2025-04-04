from django.urls import path
from . import views

app_name ='crawlings'
urlpatterns = [
    path('', views.index, name='index'),
    path('stock_debate/', views.stock_debate, name='stock_debate'),
    path('update/', views.delete_comment, name='delete_comment'),
]