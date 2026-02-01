from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tambah/', views.tambah, name='tambah'),
    path('edit/<int:id_produk>/', views.edit, name='edit'),
    path('hapus/<int:id_produk>/', views.hapus, name='hapus'),
]