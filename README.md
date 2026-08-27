# Sistema de Gestión Bomberil (Fire Department Management)

Sistema web de administración de emergencias y personal para un cuerpo de bomberos voluntarios. Originalmente desarrollado por el Cuerpo de Bomberos Voluntarios de la Universidad Simón Bolívar (CBV-USB) en 2013, y portado en este repositorio a un stack moderno (Python 3 / Django 4.2 LTS) para poder ejecutarse y evaluarse hoy.

## ¿Qué hace?

- **Gestión de personal**: registro de bomberos, rangos, ascensos, condecoraciones, cambios de condición (activo/inactivo) y permisos/vacaciones.
- **Gestión de servicios (emergencias)**: registro de servicios/emergencias atendidas, unidades y personal asignado, personas afectadas, y carga de fotos del servicio.
- **Arrestos**: registro y aprobación de horas de arresto (sanción disciplinaria) y pagos de las mismas.
- **Directorio / capital relacional**: búsqueda de personas y empresas relacionadas con el cuerpo de bomberos.
- **Estadísticas**: reportes mensuales de servicios por tipo, tiempos de respuesta y duración promedio, con gráficos.
- **Exportación a Excel**: descarga en `.xlsx` del listado de servicios (emergencias), con filtro opcional por tipo de emergencia (`/servicios/exportar/?tipo=CM`).
- **Comunicaciones**: tablón de anuncios internos del cuerpo de bomberos (`/comunicaciones/`).
- **Panel de administración** de Django para gestión de datos de bajo nivel.

## Stack técnico

- **Backend**: Python 3.11, Django 4.2 LTS
- **Base de datos**: SQLite (por defecto, configurable a MySQL)
- **Frontend**: Bootstrap 2, jQuery, plantillas de Django
- **Imágenes**: Pillow + sorl-thumbnail

## Cómo ejecutarlo localmente

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Aplicar migraciones (crea la base de datos SQLite)
python3 manage.py migrate

# 3. Crear un usuario administrador
python3 manage.py createsuperuser

# 4. Levantar el servidor de desarrollo
python3 manage.py runserver
```

Luego abre `http://localhost:8000/login/` en tu navegador.

> Nota: para que un usuario pueda ver "Mi Perfil" (`/miperfil/`) debe existir un registro de `Firefighter` (bombero) vinculado a su cuenta de usuario (`Firefighter.user`). Esto se puede crear desde `/admin/` o por consola:
> ```python
> from personal.models import Firefighter
> from django.contrib.auth.models import User
> u = User.objects.get(username='tu_usuario')
> Firefighter.objects.create(first_name='Nombre', last_name='Apellido', user=u)
> ```

## Estructura del proyecto

```
firedeptmanagement/
├── common/              # Modelos base compartidos (Persona, Dirección, Empresa, Sugerencias, etc.)
├── personal/            # Bomberos, rangos, condiciones, condecoraciones, vacaciones
├── ops/                 # Servicios (emergencias), vehículos, arrestos, exportación a Excel
├── comunicaciones/      # Tablón de anuncios internos
├── capitalrelacional/   # Directorio de personas/empresas relacionadas
├── compat_bootstrap/    # Shim local que reemplaza al paquete `django-bootstrap-toolkit` (descontinuado)
├── templates/           # Plantillas globales (404, 500, admin)
├── settings.py          # Configuración del proyecto
├── urls.py              # Enrutamiento
└── manage.py
```

## Documentación adicional

- [`docs/MIGRACION.md`](docs/MIGRACION.md): detalle técnico completo de la migración de Django 1.5/Python 2 (2013) a Django 4.2/Python 3, incluyendo todos los cambios realizados y por qué fueron necesarios.
- [`docs/CORRECCIONES.md`](docs/CORRECCIONES.md): correcciones y funcionalidades agregadas a partir de la retroalimentación de evaluación (exportación a Excel, sección de Comunicaciones, estado del despliegue).
- [`docs/video/demo_mvp.mp4`](docs/video/demo_mvp.mp4): video de demostración del MVP.

## Estado del proyecto

Este es un MVP funcional: todas las páginas principales (login, inicio, directorio, mi perfil, servicios, estadísticas, panel de administración) fueron verificadas manualmente y responden correctamente. Algunas integraciones opcionales del proyecto original (autenticación LDAP institucional, envío de correos de bienvenida) están deshabilitadas por defecto ya que dependían de configuración privada del despliegue original de la USB, no incluida en el código abierto.

## Licencia

MIT (ver encabezado del archivo `README` original).
