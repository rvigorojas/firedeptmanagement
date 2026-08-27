# Migración de Django 1.5 / Python 2 a Django 4.2 / Python 3

Este documento detalla el trabajo de migración realizado sobre el proyecto original [`saulm/firedeptmanagement`](https://github.com/saulm/firedeptmanagement) (2013, marcado por su autor como "no longer maintained") para que pudiera ejecutarse en un entorno actual.

## Contexto original

El proyecto usaba:
- Django 1.5 (2013), con sintaxis de URLs basada en `django.conf.urls.patterns()` y vistas referenciadas como strings.
- Python 2 (uso de `unicode()`, `__unicode__`, `.iteritems()`, `print` como sentencia, etc.).
- `South` para migraciones de base de datos (reemplazado por migraciones nativas de Django desde la versión 1.7).
- `python-ldap` / `django-auth-ldap` para autenticación institucional contra un servidor LDAP privado de la USB.
- `django-bootstrap-toolkit`, un paquete ya no publicado en PyPI.
- Un `local_settings.py` privado (nunca publicado en el repositorio original) del que dependían funciones como el envío de correos de bienvenida.

## Cambios realizados

### 1. Estructura de imports
El código mezclaba imports absolutos con prefijo (`firedeptmanagement.common.views`) e imports planos (`common.views`) de forma inconsistente, lo cual ya rompía la ejecución en el propio Python 2. Se normalizaron todos los imports a la forma plana (`common`, `personal`, `ops`, `capitalrelacional`), consistente con cómo `manage.py` carga `settings`.

### 2. `urls.py`
Reescrito por completo:
- `django.conf.urls.patterns()` (eliminado en Django 1.10) → lista de `path()` / `re_path()`.
- Vistas referenciadas por string (`'common.views.base'`) → imports directos de las funciones de vista.
- `django.contrib.auth.views.login` (función, eliminada) → `django.contrib.auth.views.LoginView.as_view(...)`.

### 3. `settings.py`
- `TEMPLATE_LOADERS` / `TEMPLATE_DIRS` / `TEMPLATE_CONTEXT_PROCESSORS` (eliminados en Django 1.8) → un único setting `TEMPLATES`.
- `MIDDLEWARE_CLASSES` → `MIDDLEWARE`.
- Se agregaron `SECRET_KEY`, `ALLOWED_HOSTS`, `DEFAULT_AUTO_FIELD` (requeridos por versiones modernas de Django).
- Se agregaron valores por defecto para settings que el código esperaba pero que solo existían en el `local_settings.py` privado del despliegue original: `MAPS_API_KEY`, `GA`, `BAJ_CONDITION`, `SUGGESTION_MAIL_*`.
- Se removieron `south` y `django-bootstrap-toolkit` de `INSTALLED_APPS`, reemplazando este último por una app local (`compat_bootstrap`).

### 4. Modelos (`models.py` en cada app)
- Se agregó `on_delete=models.CASCADE` a las ~44 `ForeignKey`/`OneToOneField` que no lo tenían (obligatorio desde Django 2.0).
- `__unicode__` → `__str__` (Python 2 vs. 3).
- `unicode(x)` → `str(x)`.
- Se agregó `fields = [...]` a un `ModelForm` (`SuggestionForm`) que no declaraba ni `fields` ni `exclude`, requerido desde Django 1.8.

### 5. Vistas (`views.py` en cada app)
- `render_to_response(template, RequestContext(request, ctx))` (eliminado en Django 3.0) → `render(request, template, ctx)`.
- `request.user.get_profile()` (mecanismo de perfil de usuario, eliminado en Django 1.7) → `request.user.firefighter` (accessor inverso del `OneToOneField` en el modelo `Firefighter`).
- `@transaction.commit_on_success` (eliminado en Django 1.8) → `@transaction.atomic`.
- `django.utils.datastructures.SortedDict` (eliminado; innecesario desde Python 3.7, los `dict` mantienen orden de inserción) → `collections.OrderedDict`.
- `connection.ops.date_trunc_sql(...)` con SQL crudo (firma cambiada en Django moderno) → función ORM `django.db.models.functions.TruncMonth`, portable entre motores de base de datos.
- `filter(lambda ...)` sobre el que luego se llamaba `len()` (en Python 3 `filter` devuelve un iterador sin `len`) → envuelto en `list(...)`.
- `.iteritems()` → `.items()`.

### 6. Autenticación LDAP institucional
El código original creaba automáticamente cuentas LDAP al crear un `Firefighter`, usando credenciales del servidor LDAP de la USB (`AUTH_LDAP_*`), nunca incluidas en el repositorio público. Esta función se dejó **deshabilitada por defecto** (se activa solo si se configura `AUTH_LDAP_BIND_PASSWORD`), documentado explícitamente en `personal/models.py`. Los imports de `django_auth_ldap` se movieron dentro del bloque condicional para no requerir el paquete cuando la función está apagada.

### 7. `utils/passwords.py`
`base64.encodestring` (eliminado en Python 3.9) → `base64.encodebytes`.

### 8. Migraciones de base de datos
Se eliminaron todas las migraciones de `South` (`0001_initial.py`, etc. con formato antiguo) y se regeneraron migraciones nativas de Django con `manage.py makemigrations`.

### 9. Plantillas HTML
- `{% url 'django.contrib.auth.views.login' %}` → `{% url 'login' %}` (los nombres de URL cambiaron al reescribir `urls.py`).
- Se agregó un alias de URL `frontpage` (usado en `templates/404.html`) apuntando a la misma vista que `base`.

### 10. `compat_bootstrap/`
App local mínima que reemplaza al filtro `as_bootstrap` de `django-bootstrap-toolkit` (paquete descontinuado, no disponible en PyPI), usado en las plantillas de `ops/templates/` para renderizar formularios con clases de Bootstrap 2.

## Verificación

Se probaron manualmente (con sesión autenticada) todas las rutas principales, confirmando código de respuesta `200 OK`:

| Ruta | Función |
|---|---|
| `/login/` | Inicio de sesión |
| `/` | Panel de inicio |
| `/admin/` | Panel de administración de Django |
| `/directorio/` | Directorio / capital relacional |
| `/miperfil/` | Perfil del bombero |
| `/servicios/` | Listado de servicios (emergencias) |
| `/estadisticas/` | Estadísticas mensuales |
| `/estadisticas/plain/` | Estadísticas (versión sin adornos) |
| `/static/...` | Archivos estáticos (CSS/JS/imágenes) |

## Limitaciones conocidas

- La integración LDAP y el envío real de correos (bienvenida, notificaciones al webmaster) están deshabilitados por no contar con las credenciales/infraestructura privada del despliegue original.
- No se migraron datos del despliegue original (no estaban disponibles); la base de datos se genera vacía y se debe poblar manualmente o desde `/admin/`.
- La app `opera` (integración con un sistema externo de "expedientes") ya venía deshabilitada en el proyecto original (`#'opera'` comentado en `INSTALLED_APPS`) y se mantuvo así.
