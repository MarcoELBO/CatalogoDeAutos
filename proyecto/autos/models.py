from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
#Clase Usuario
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    #Duda de por que solo se pone el nombre en el str
    def __str__(self):
        return self.nombre
    #Duda el por que se utiliza el Meta
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

#Clase Vendedor
class Vendedor(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, help_text="Tipo de vendedor: Agencia, Privado, Concesionario")
    email = models.EmailField(max_length=100, unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    def __str__(self):
        return f"{self.nombre}({self.tipo})"
    class Meta:
        verbose_name = "Vendedor"
        verbose_name_plural = "Vendedores"

#Clase Auto
class Auto(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField(verbose_name="Año de fabricación")
    version = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=30)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    kilometraje = models.IntegerField(help_text="Kilometraje en kilómetros")
    estado = models.CharField(max_length=10, help_text="Estado del auto: Nuevo, Usado")
    imagen_auto = models.ImageField(upload_to='autos/', blank=True, null=True, verbose_name="Imagen del auto")
    
    #Foreignkey a Vendedor
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name="autos", verbose_name="Vendedor")
    
    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.anio})"
    class Meta:
        verbose_name = "Auto"
        verbose_name_plural = "Autos"
        ordering = ['-anio', 'marca', 'modelo']

#Clase Consulta
class Consulta(models.Model):
    fecha_consulta = models.DateTimeField(auto_now_add=True)
    #Foreignkey a Usuario
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="consultas")
    #Foreignkey a Auto
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name="consultas")

    def __str__(self):
        return f"Consulta de {self.usuario.nombre} sobre {self.auto.marca} {self.auto.modelo} el {self.fecha_consulta.strftime('%Y-%m-%d %H:%M:%S')}"
    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        ordering = ['-fecha_consulta']

class Resena(models.Model):
    comentario = models.TextField()
    puntuacion = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)] ,help_text="Puntuación del 1 al 5")
    fecha_resena = models.DateTimeField(auto_now_add=True)
    #Foreignkey a Usuario
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="resenas")
    #Foreignkey a Auto
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name="resenas")
    def __str__(self):
        return f"Reseña de {self.usuario.nombre} sobre {self.auto.marca} {self.auto.modelo} - Puntuación: {self.puntuacion}"
    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ['-fecha_resena']


                                
