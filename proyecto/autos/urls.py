from django.urls import path
from django.views.generic import TemplateView
from .views import InicioView, MenuView

urlpatterns = [
    path('', InicioView.as_view(), name='inicio'),  # Vista de la página de inicio
    path('menu/', MenuView.as_view(), name='menu'),
    path('faqs/', TemplateView.as_view(template_name='autos/faqs.html'), name='faqs'),  # Página de FAQs estática
]