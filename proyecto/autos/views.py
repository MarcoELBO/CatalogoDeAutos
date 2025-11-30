from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
# IMPORTANTE: Importamos Resena
from .models import Auto, Usuario, Resena 
from django.contrib.auth.models import User as UserDjango 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

# ... (InicioView y MenuView se quedan igual) ...

class InicioView(ListView):
    model = Auto
    template_name = 'autos/inicio.html'
    context_object_name = 'featured_cars' 

    def get_queryset(self):
        return Auto.objects.all().order_by('-anio')[:3]

class MenuView(ListView):
    model = Auto
    template_name = 'autos/menu.html'
    context_object_name = 'autos'
    paginate_by = 16

    def get_queryset(self):
        queryset = super().get_queryset().select_related('vendedor')
        search_query = self.request.GET.get('q')
        
        if search_query:
            queryset = queryset.filter(
                Q(marca__icontains=search_query) | 
                Q(modelo__icontains=search_query)
            )

        marca_filter = self.request.GET.get('marca')
        precio_max_filter = self.request.GET.get('precio_max')

        if marca_filter:
            queryset = queryset.filter(marca__icontains=marca_filter)

        if precio_max_filter:
            try:
                queryset = queryset.filter(precio__lte=precio_max_filter)
            except ValueError:
                pass 

        orden = self.request.GET.get('ordenar', 'relevantes')

        if orden == 'precio_asc':
            queryset = queryset.order_by('precio')
        elif orden == 'precio_desc':
            queryset = queryset.order_by('-precio')
        elif orden == 'ano_desc':
            queryset = queryset.order_by('-ano')
        else:
            queryset = queryset.order_by(*self.model._meta.ordering)
        
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orden_actual'] = self.request.GET.get('ordenar', 'relevantes')
        context['marca_actual'] = self.request.GET.get('marca', '')
        context['precio_max_actual'] = self.request.GET.get('precio_max', '')
        context['search_actual'] = self.request.GET.get('q', '')
        return context

# --- VISTA DE DETALLE ACTUALIZADA (Maneja Reseñas) ---
class AutoDetalleView(DetailView):
    model = Auto
    template_name = 'autos/auto_detalle.html' 
    context_object_name = 'auto'

    def post(self, request, *args, **kwargs):
        # 1. Validar login
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para dejar una reseña.")
            return redirect('login')
        
        self.object = self.get_object()
        auto = self.object

        # 2. Obtener datos
        puntuacion = request.POST.get('puntuacion')
        comentario = request.POST.get('comentario')

        if not puntuacion or not comentario:
            messages.error(request, "Por favor califica y escribe un comentario.")
            return redirect('auto_detalle', pk=auto.pk)

        # 3. Buscar Usuario Personalizado
        try:
            # Buscamos por email para enlazar el User de Django con tu modelo Usuario
            usuario_personalizado = Usuario.objects.get(email=request.user.email)
        except Usuario.DoesNotExist:
            # Si eres admin y no tienes perfil, lo creamos temporalmente para evitar error
            usuario_personalizado = Usuario.objects.create(
                nombre=request.user.username, 
                email=request.user.email,
                telefono="0000000000"
            )

        # 4. Guardar
        Resena.objects.create(
            auto=auto,
            usuario=usuario_personalizado,
            puntuacion=int(puntuacion),
            comentario=comentario
        )

        messages.success(request, "¡Tu reseña ha sido publicada!")
        return redirect('auto_detalle', pk=auto.pk)


# ... (El resto de vistas: CompararView, toggle_comparar, Favoritos, Auth, etc. se quedan igual) ...

class CompararView(TemplateView):
    template_name = 'autos/comparar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista_ids = self.request.session.get('comparacion_ids', [])
        
        if lista_ids:
            context['autos_comparar'] = Auto.objects.filter(id__in=lista_ids)
        else:
            context['autos_comparar'] = []
            
        return context

def toggle_comparar(request, pk):
    lista_ids = request.session.get('comparacion_ids', [])
    if pk in lista_ids:
        lista_ids.remove(pk)
        messages.info(request, "Auto eliminado de la comparación.")
    else:
        if len(lista_ids) < 3:
            lista_ids.append(pk)
            messages.success(request, "Auto agregado para comparar.")
        else:
            messages.warning(request, "Solo puedes comparar hasta 3 autos a la vez.")
    request.session['comparacion_ids'] = lista_ids
    return redirect(request.META.get('HTTP_REFERER', 'menu'))

class FavoritosView(ListView):
    model = Auto
    template_name = 'autos/favoritos.html'
    context_object_name = 'autos'

    def get_queryset(self):
        lista_ids = self.request.session.get('favoritos_ids', [])
        return Auto.objects.filter(id__in=lista_ids)

def toggle_favorito(request, pk):
    favs = request.session.get('favoritos_ids', [])
    if pk in favs:
        favs.remove(pk)
        messages.info(request, "Eliminado de favoritos.")
    else:
        favs.append(pk)
        messages.success(request, "¡Agregado a favoritos!")
    request.session['favoritos_ids'] = favs
    return redirect(request.META.get('HTTP_REFERER', 'menu'))

def registro_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo') 
        telefono = request.POST.get('telefono')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password2')

        if password != password_confirm:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, 'autos/register.html')
        
        if UserDjango.objects.filter(email=correo).exists() or Usuario.objects.filter(email=correo).exists():
            messages.error(request, "Este correo ya está registrado")
            return render(request, 'autos/register.html')

        try:
            user_django = UserDjango.objects.create_user(
                username=correo, email=correo, password=password, first_name=nombre
            )
            user_django.save()

            usuario_personalizado = Usuario(
                nombre=nombre, email=correo, telefono=telefono
            )
            usuario_personalizado.save()
            
            messages.success(request, "¡Cuenta creada! Datos guardados correctamente.")
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f"Ocurrió un error: {e}")
            return render(request, 'autos/register.html')

    return render(request, 'autos/register.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio') 
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, 'autos/login.html')

def logout_view(request):
    logout(request)
    return redirect('menu')