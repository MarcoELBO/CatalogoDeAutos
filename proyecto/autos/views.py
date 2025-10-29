from django.views.generic import ListView
from .models import Auto

# Create your views here.
class InicioView(ListView):
    model = Auto
    template_name = 'autos/inicio.html'
    # El HTML de inicio espera una variable llamada 'featured_cars'
    context_object_name = 'featured_cars' 

    def get_queryset(self):
        # Obtenemos los 3 autos más nuevos
        return Auto.objects.all().order_by('-anio')[:3]

class MenuView(ListView):
    model = Auto
    template_name = 'autos/menu.html'
    context_object_name = 'autos'
    paginate_by = 12  # Número de autos por página

    def get_queryset(self):
        queryset = super().get_queryset().select_related('vendedor')

        orden = self.request.GET.get('orden', 'relevantes')

        if orden == 'precio_asc':
            queryset = queryset.order_by('precio')
        elif orden == 'precio_desc':
            queryset = queryset.order_by('-precio')
        elif orden == 'anio_desc':
            queryset = queryset.order_by('-anio')
        else:
            queryset = queryset.order_by(*self.model._meta.ordering)
        
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orden_actual'] = self.request.GET.get('orden', 'relevantes')
        return context
