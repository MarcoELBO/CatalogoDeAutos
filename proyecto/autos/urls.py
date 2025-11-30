from django.urls import path
from django.views.generic import TemplateView
from .views import InicioView, MenuView, AutoDetalleView, CompararView, toggle_comparar, registro_view, login_view, logout_view, FavoritosView, toggle_favorito

urlpatterns = [
    path('', InicioView.as_view(), name='inicio'),  # Vista de la página de inicio
    path('menu/', MenuView.as_view(), name='menu'),
    path('faqs/', TemplateView.as_view(template_name='autos/faqs.html'), name='faqs'),  # Página de FAQs estática
    path('registro/', registro_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('auto/<int:pk>/', AutoDetalleView.as_view(), name='auto_detalle'),
    path('comparar/', CompararView.as_view(), name='comparar'),
    path('comparar/toggle/<int:pk>/', toggle_comparar, name='toggle_comparar'),
    path('favoritos/', FavoritosView.as_view(), name='favoritos'),
    path('favoritos/toggle/<int:pk>/', toggle_favorito, name='toggle_favorito'),
    path('favoritos/', FavoritosView.as_view(), name='favoritos'),
    
]
