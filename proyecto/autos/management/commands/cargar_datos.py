from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from autos.models import Vendedor, Auto
import os


class Command(BaseCommand):
    help = 'Carga 15 vendedores y 15 autos de ejemplo en la base de datos (incluye imágenes si están disponibles)'

    def add_arguments(self, parser):
        parser.add_argument('--no-images', action='store_true', help='No intentar cargar imágenes aunque existan')

    def handle(self, *args, **options):
        no_images = options.get('no_images', False)

        # Crear 15 vendedores
        vendedores = []
        for i in range(1, 16):
            v_data = {
                'nombre': f'Vendedor {i}',
                'tipo': 'Concesionario' if i % 3 == 0 else 'Agencia' if i % 3 == 1 else 'Privado',
                'email': f'vendedor{i}@example.com',
                'telefono': f'555-{1000 + i}'
            }
            v, _ = Vendedor.objects.get_or_create(email=v_data['email'], defaults=v_data)
            vendedores.append(v)

        # Directorio donde el comando buscará imágenes de ejemplo
        imagenes_dir = os.path.join(settings.BASE_DIR, 'autos', 'datos_ejemplo', 'imagenes')

        # Mapado de marcas a modelos reales para generar datos más verosímiles
        modelos_por_marca = {
            'Toyota': ['Corolla', 'Camry', 'RAV4'],
            'Honda': ['Civic', 'Accord', 'CR-V'],
            'Volkswagen': ['Golf', 'Polo', 'Passat'],
            'Ford': ['Focus', 'Fiesta', 'Mustang'],
            'Chevrolet': ['Cruze', 'Camaro', 'Spark'],
            'Nissan': ['Sentra', 'Altima', 'Qashqai'],
            'Hyundai': ['Elantra', 'Tucson', 'i30'],
            'Kia': ['Rio', 'Sportage', 'Ceed'],
            'BMW': ['Serie3', 'Serie5', 'X3'],
            'Mercedes': ['C-Class', 'E-Class', 'GLA'],
            'Audi': ['A3', 'A4', 'Q3'],
            'Renault': ['Clio', 'Megane', 'Captur'],
            'Peugeot': ['208', '308', '3008'],
            'Mazda': ['Mazda2', 'Mazda3', 'CX-5'],
            'Subaru': ['Impreza', 'Forester', 'Outback'],
        }

        marcas = list(modelos_por_marca.keys())
        colores = ['Rojo', 'Azul', 'Negro', 'Blanco', 'Gris']

        # Crear 15 autos
        for i in range(1, 16):
            marca = marcas[(i - 1) % len(marcas)]
            # elegir un modelo real para la marca
            modelos = modelos_por_marca.get(marca, [f'Model{i}'])
            modelo = modelos[(i - 1) % len(modelos)]
            anio = 2024 - ((i - 1) % 6)  # cicla entre 2019-2024 aproximadamente
            version = f'{modelo} {i % 3 + 1}'
            color = colores[i % len(colores)]
            precio = 12000.00 + i * 1000
            kilometraje = 0 if i % 2 == 0 else i * 1000
            estado = 'Nuevo' if kilometraje == 0 else 'Usado'
            vendedor = vendedores[(i - 1) % len(vendedores)]
            imagen_nombre = f"{marca.lower()}_{i}.jpg"

            defaults = {
                'marca': marca,
                'modelo': modelo,
                'anio': anio,
                'version': version,
                'color': color,
                'precio': precio,
                'kilometraje': kilometraje,
                'estado': estado,
                'vendedor': vendedor,
            }

            auto, created = Auto.objects.get_or_create(marca=marca, modelo=modelo, anio=anio, vendedor=vendedor, defaults=defaults)

            # Intentar añadir imagen si existe y no se pidió omitir imágenes
            if not no_images:
                posible_path = os.path.join(imagenes_dir, imagen_nombre)
                if os.path.exists(posible_path):
                    try:
                        with open(posible_path, 'rb') as f:
                            nuevo_nombre = f"{auto.marca}_{auto.modelo}_{auto.id}{os.path.splitext(imagen_nombre)[1]}"
                            auto.imagen_auto.save(nuevo_nombre, File(f), save=True)
                    except Exception as e:
                        self.stderr.write(self.style.WARNING(f"No se pudo guardar la imagen {imagen_nombre}: {e}"))
                else:
                    # No es un error, solo aviso informativo
                    self.stdout.write(self.style.NOTICE(f"Imagen no encontrada: {posible_path} (no se cargará)"))

        self.stdout.write(self.style.SUCCESS('Se han cargado 15 vendedores y 15 autos (si no existían)'))