from django.core.management.base import BaseCommand
from catalogo.models import Auto, Vendedor

class Command(BaseCommand):
    help = 'Carga una lista inicial de autos en la base de datos'

    def handle(self, *args, **kwargs):
        # 1. Aseguramos que exista al menos un vendedor para asignar los autos
        vendedor, created = Vendedor.objects.get_or_create(
            nombre="Agencia Vukimotors",
            defaults={
                "tipo": "Agencia",
                "correo": "ventas@vukimotors.com",
                "telefono": "555-0123"
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Se creó el vendedor: {vendedor.nombre}'))
        else:
            self.stdout.write(f'Usando vendedor existente: {vendedor.nombre}')

        # 2. Tu lista de autos (JSON)
        autos_data = [
            {
                "marca": "Ford",
                "modelo": "Ranger",
                "año": 2025,
                "versión": "Wildtrak Double Cab 4×4",
                "color": "Gris oscuro metálico",
                "precio_mxn": 960900,
                "kilometraje": 10000,
                "estado": "Seminuevo"
            },
            {
                "marca": "Ford",
                "modelo": "Maverick",
                "año": 2025,
                "versión": "XLT Híbrida",
                "color": "Blanco perla",
                "precio_mxn": 752100,
                "kilometraje": 5000,
                "estado": "Nuevo"
            },
            {
                "marca": "Ford",
                "modelo": "Bronco Sport",
                "año": 2025,
                "versión": "Outer Banks",
                "color": "Rojo desierto",
                "precio_mxn": 859000,
                "kilometraje": 15000,
                "estado": "Seminuevo"
            },
            {
                "marca": "Chevrolet",
                "modelo": "Aveo",
                "año": 2024,
                "versión": "LS Sedán",
                "color": "Blanco clásico",
                "precio_mxn": 320000,
                "kilometraje": 20000,
                "estado": "Usado"
            },
            {
                "marca": "Chevrolet",
                "modelo": "Blazer",
                "año": 2025,
                "versión": "V6 3.6L",
                "color": "Azul tormenta/negro",
                "precio_mxn": 990900,
                "kilometraje": 8000,
                "estado": "Nuevo"
            },
            {
                "marca": "Chevrolet",
                "modelo": "Silverado",
                "año": 2024,
                "versión": "Trail Boss",
                "color": "Negro",
                "precio_mxn": 1200000,
                "kilometraje": 25000,
                "estado": "Seminuevo"
            },
            {
                "marca": "Nissan",
                "modelo": "Versa",
                "año": 2025,
                "versión": "Advance CVT",
                "color": "Azul marino",
                "precio_mxn": 411900,
                "kilometraje": 7000,
                "estado": "Seminuevo"
            },
            {
                "marca": "Nissan",
                "modelo": "Kicks",
                "año": 2024,
                "versión": "SR",
                "color": "Rojo fuego",
                "precio_mxn": 485000,
                "kilometraje": 12000,
                "estado": "Usado"
            },
            {
                "marca": "Nissan",
                "modelo": "NP300",
                "año": 2023,
                "versión": "Cabina Doble 4×2",
                "color": "Blanco",
                "precio_mxn": 430000,
                "kilometraje": 30000,
                "estado": "Usado"
            },
            {
                "marca": "Volkswagen",
                "modelo": "Jetta",
                "año": 2025,
                "versión": "GLI",
                "color": "Rojo Tornado / Negro",
                "precio_mxn": 480000,
                "kilometraje": 6000,
                "estado": "Nuevo"
            },
            {
                "marca": "Volkswagen",
                "modelo": "Taos",
                "año": 2024,
                "versión": "Trendline",
                "color": "Blanco puro",
                "precio_mxn": 420000,
                "kilometraje": 14000,
                "estado": "Seminuevo"
            },
            {
                "marca": "Volkswagen",
                "modelo": "Tiguan",
                "año": 2025,
                "versión": "Comfortline",
                "color": "Azul Monterey",
                "precio_mxn": 677990,
                "kilometraje": 12000,
                "estado": "Seminuevo"
            },
            {
                "marca": "Kia",
                "modelo": "K3",
                "año": 2025,
                "versión": "L TA",
                "color": "Plata lunar",
                "precio_mxn": 322400,
                "kilometraje": 4000,
                "estado": "Nuevo"
            },
            {
                "marca": "Kia",
                "modelo": "Seltos",
                "año": 2024,
                "versión": "EX CVT",
                "color": "Gris titanio",
                "precio_mxn": 420000,
                "kilometraje": 15000,
                "estado": "Usado"
            },
            {
                "marca": "Kia",
                "modelo": "Forte",
                "año": 2025,
                "versión": "GT",
                "color": "Negro brillante",
                "precio_mxn": 482000,
                "kilometraje": 5000,
                "estado": "Seminuevo"
            }
        ]

        # 3. Iterar y Guardar
        contador = 0
        for data in autos_data:
            # Verificamos si el auto ya existe para no duplicarlo (opcional)
            if not Auto.objects.filter(marca=data['marca'], modelo=data['modelo'], anio=data['año'], vendedor=vendedor).exists():
                Auto.objects.create(
                    marca=data['marca'],
                    modelo=data['modelo'],
                    anio=data['año'],          # Mapeamos 'año' del JSON a 'anio' del modelo
                    version=data['versión'],   # Mapeamos 'versión' a 'version'
                    color=data['color'],
                    precio=data['precio_mxn'], # Mapeamos 'precio_mxn' a 'precio'
                    kilometraje=data['kilometraje'],
                    estado=data['estado'],
                    vendedor=vendedor          # Asignamos el vendedor
                )
                self.stdout.write(f"Guardado: {data['marca']} {data['modelo']}")
                contador += 1
            else:
                self.stdout.write(self.style.WARNING(f"Saltado (ya existe): {data['marca']} {data['modelo']}"))

        self.stdout.write(self.style.SUCCESS(f'¡Proceso terminado! Se agregaron {contador} autos.'))