# Correcciones aplicadas tras retroalimentación de evaluación

Este documento registra los cambios hechos al proyecto a partir de los comentarios
recibidos en la sesión de evaluación/avance (transcripción de reunión entre
evaluador y estudiante), previos a la entrega final. El objetivo es dejar
trazabilidad de qué se pidió y qué se hizo al respecto, en vez de mezclarlo
silenciosamente con el resto del código.

## Resumen de lo pedido en la reunión

De la transcripción (con ruido propio de una transcripción automática) se
identificaron los siguientes puntos:

1. Agregar una forma de **exportar a Excel** los datos del sistema, filtrado o
   segmentado **por tipo de emergencia**.
2. Se señaló que existe una **sección de "Comunicaciones"** en la interfaz que
   está vacía / sin desarrollar, y se pidió completarla.
3. El evaluador preguntó **dónde está desplegada / hospedada** la aplicación, y
   el estudiante no tenía una respuesta clara.
4. Advertencia general del evaluador sobre **no delegar todo el trabajo a una
   IA** sin entender o justificar las decisiones tomadas.
5. Sugerencia de usar una herramienta externa ("Stitch") para mejorar el
   diseño visual a partir de capturas de pantalla y el PRD del proyecto.
6. Se mencionó un plazo de aproximadamente **una semana** para la entrega.

## 1. Exportación a Excel — implementado

Se agregó la vista `ops.views.export_services_excel`, expuesta en
`/servicios/exportar/`, que genera un archivo `.xlsx` (usando `openpyxl`) con
el listado de servicios (emergencias) registrados: fecha, hora, tipo,
descripción, ubicación, tiempo de respuesta y duración.

Acepta un parámetro opcional `?tipo=<código>` (los mismos códigos que
`Service.SERVICE_TYPE_CHOICES`, p. ej. `CM`, `IDE`, `RES1`) para filtrar la
exportación a un solo tipo de emergencia. Si no se especifica, exporta todos
los tipos.

En la pantalla de **Servicios** (`/servicios/`) se agregó un selector de tipo
de emergencia junto a un botón "Exportar" que arma esa URL automáticamente,
para que no sea necesario escribir el parámetro a mano.

Verificado manualmente: exportación sin filtro y con `?tipo=CM` devuelven un
`.xlsx` válido (confirmado abriendo el archivo con `openpyxl` y leyendo sus
filas).

## 2. Sección "Comunicaciones" — implementado como interpretación razonable, sujeta a confirmación

En el código heredado del proyecto original **no existía ningún rastro** de
una sección de "Comunicaciones" (ni modelo, ni vista, ni plantilla, ni enlace
en el menú) — se verificó con una búsqueda exhaustiva en todo el repositorio.
Es decir, no es que estuviera "vacía": no estaba implementada en absoluto.

Dado que no había especificación de qué debía contener, se optó por construir
la interpretación más común para un sistema de gestión de un cuerpo de
bomberos: un **tablón de anuncios internos** donde cualquier bombero con
sesión iniciada puede publicar y leer comunicados (por ejemplo: convocatorias
a reuniones, avisos de guardia, anuncios administrativos).

Se agregó una app nueva, `comunicaciones/`, con:

- Modelo `Communication` (título, contenido, autor, fecha de publicación,
  bandera "fijada" para anuncios importantes).
- Vista de listado en `/comunicaciones/` (más recientes primero, fijados
  arriba).
- Vista de creación en `/comunicaciones/nueva/`.
- Enlace nuevo en el menú principal ("Comunicaciones").
- Registrado en el panel de administración de Django.

**Esto es una decisión de diseño tomada por interpretación, no una
transcripción literal de un requisito confirmado.** Si la sección debía tener
otro propósito (por ejemplo: comunicaciones con la comunidad externa,
bitácora de radio, registro de llamadas de emergencia entrantes, etc.), el
modelo y las vistas están aisladas en su propia app y son fáciles de ajustar
o reemplazar sin tocar el resto del sistema.

## 3. Despliegue — pendiente, requiere una decisión del equipo

La aplicación, tal como está en este repositorio, **corre localmente**
(`python3 manage.py runserver`) pero no está desplegada en ningún servidor
público con URL permanente. Esto no se resolvió como parte de estas
correcciones porque desplegarla implica crear una cuenta en un proveedor de
hosting (Render, Railway, PythonAnywhere, Fly.io, etc.), lo cual requiere
que lo haga una persona del equipo (no puede hacerse de forma automatizada
en nombre de terceros).

Pasos sugeridos para hacerlo antes de la entrega (usando Render como
ejemplo, por tener capa gratuita y despliegue directo desde GitHub):

1. Crear una cuenta en [render.com](https://render.com) y conectarla a la
   cuenta de GitHub donde está este repositorio.
2. Crear un "Web Service" nuevo apuntando a este repositorio.
3. Comando de build: `pip install -r requirements.txt`.
4. Comando de arranque: `gunicorn urls:application` — **nota**: hace falta
   agregar `gunicorn` a `requirements.txt` y ajustar `ALLOWED_HOSTS` en
   `settings.py` al dominio que asigne Render (además de establecer
   `DEBUG = False` y una `SECRET_KEY` real vía variable de entorno antes de
   exponerlo públicamente).
5. Ejecutar `python3 manage.py migrate` y `python3 manage.py createsuperuser`
   contra la base de datos del servicio desplegado (Render provee una
   consola/shell para esto).

Se dejó fuera del alcance de esta corrección automática porque involucra
credenciales y decisiones (proveedor, dominio, presupuesto) que le
corresponden al equipo, no a un cambio de código.

## 4. Sobre el uso de IA en el proyecto

El comentario del evaluador sobre no delegar todo el trabajo a una IA sin
entenderlo aplica directamente a este mismo proceso: por eso este documento
existe — para que quede explícito qué se le pidió a la IA, qué decisiones
tomó por su cuenta (como el contenido de "Comunicaciones", marcado arriba) y
qué quedó pendiente de decisión humana (el despliegue). El estudiante debe
poder explicar cada uno de estos cambios en la evaluación, no solo entregarlos.

## 5. Mejora visual con "Stitch" — no aplicado

Es un paso manual que le corresponde al equipo: generar capturas de pantalla
del sistema actual, escribir o adjuntar el PRD, y pasarlo por esa herramienta
externa de diseño. El resultado (mockups o especificaciones de estilo) puede
traerse de vuelta para aplicar cambios puntuales de CSS/plantillas, pero no
hay nada que una IA pueda generar aquí sin ese insumo visual primero.

## 6. Integración del diseño de Stitch — implementado

El diseño de referencia generado con Stitch ("SSEI Aeroportuario", 5 pantallas:
Dashboard escritorio, Dashboard móvil, Listado de Servicios, Tablón de
Anuncios y Estadísticas) se integró a la aplicación real (Django), en lugar
de quedar solo como un mockup separado. Cambios concretos:

- **Identidad/marca**: el encabezado del sitio (`settings.SITE_HEADER`) y el
  `<title>` pasaron de "Cuerpo de Bomberos Voluntarios — Universidad Simón
  Bolívar" a **"SSEI Aeroportuario — Servicio de Salvamento y Extinción de
  Incendios / Base SSEI - Operacional"**.
- **Tema visual**: se agregó `staticfiles/css/ssei_theme.css`, una hoja de
  estilos oscura (azul marino / naranja-rojo) que se carga después de
  `style.css` y reestiliza navbar, tablas, alertas, botones y formularios
  para que coincidan con la paleta del diseño de Stitch, sin reescribir el
  layout heredado de Bootstrap 2 del proyecto original.
- **Tipos de incidente**: `Service.SERVICE_TYPE_CHOICES` (en `ops/models.py`)
  se actualizó para reflejar operativa aeroportuaria real: *Falla de
  Aeronave*, *Derrame de Combustible (Jet-A1)*, *Emergencia Médica
  (Terminal/Plataforma)*, *Incendio en Estructura/Plataforma*, *Falsa Alarma*
  y *Simulacro Regulatorio (RAP 314/OACI)*. Los códigos originales del
  proyecto 2013 se conservaron al final de la lista por compatibilidad
  (migración `ops/0002_alter_service_service_type`).
- **Tablero (Dashboard) operativo**: la vista `common.views.base` ahora
  calcula indicadores tipo "Centro de Mando" (incidentes activos, unidades
  desplegadas, personal de turno, tiempo promedio de respuesta) que se
  muestran como tarjetas en `inicio.html`, igual que en el diseño de Stitch.
- **Datos de ejemplo**: los servicios de demostración se reemplazaron por
  escenarios aeroportuarios (falla de tren de aterrizaje en Pista 10L,
  derrame de Jet-A1 en Plataforma Sur, simulacro RAP 314 en Sector Pista,
  etc.) para que el video y las capturas sean consistentes con la nueva
  identidad.
- **Video de demostración**: se regrabó (`docs/video/demo_mvp.mp4`) sobre la
  aplicación ya con el nuevo tema y los nuevos datos de ejemplo.

Lo que **no** se hizo, por alcance/tiempo: no se reconstruyó el layout como
un sidebar fijo pixel-a-pixel idéntico al mockup de Stitch (la app sigue
usando el navbar superior heredado de 2013); la identidad, terminología, tema
de color y contenido operativo sí quedaron alineados. Si se requiere fidelidad
visual 1:1 con el mockup, el siguiente paso sería un rediseño de layout más
profundo (barra lateral fija, tarjetas con esquinas redondeadas idénticas,
etc.), fuera del alcance de esta corrección.

## Verificación posterior a estos cambios

Se repitió la verificación manual de rutas (sesión autenticada, servidor
local) incluyendo las nuevas: `/comunicaciones/`, `/comunicaciones/nueva/`
(GET y POST de creación) y `/servicios/exportar/` (sin filtro y con
`?tipo=CM`), además de las rutas ya verificadas en
[`docs/MIGRACION.md`](MIGRACION.md). Todas responden `200 OK`, y el archivo
`.xlsx` generado se abrió y verificó con `openpyxl`.

Tras la integración del diseño de Stitch (sección 6) se repitió el barrido
completo de rutas (`/`, `/servicios/`, `/comunicaciones/`,
`/comunicaciones/nueva/`, `/estadisticas/`, `/directorio/`, `/miperfil/`,
`/servicios/exportar/`, `/admin/`) con sesión autenticada: todas responden
`200 OK` después de aplicar la migración `ops/0002_alter_service_service_type`.
