from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from django.views.static import serve as static_serve

from common import views as common_views
from capitalrelacional import views as capitalrelacional_views
from personal import views as personal_views
from ops import views as ops_views
from comunicaciones import views as comunicaciones_views

admin.autodiscover()

urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),
    path('', common_views.base, name='base'),
    path('', common_views.base, name='frontpage'),
    path('estadisticas/', ops_views.statistics, name='statistics'),
    path('estadisticas/plain/', ops_views.plain_statistics, name='plain_statistics'),
    re_path(r'^estadisticas/(?P<year>\d+)-(?P<month>\d+)/$', ops_views.month_statistics, name='month_statistics'),
    re_path(r'^estadisticas/plain/(?P<year>\d+)-(?P<month>\d+)/$', ops_views.month_statistics, name='month_statistics_plain'),
    re_path(r'^estadisticas/detalle/(?P<year>\d+)-(?P<month>\d+)/$', ops_views.month_statistics_detail, name='month_statistics_detail'),
    re_path(r'^estadisticas/plain/detalle/(?P<year>\d+)-(?P<month>\d+)/$', ops_views.month_statistics_detail, name='month_statistics_detail_plain'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGIN_URL), name='logout'),
    path('directorio/', capitalrelacional_views.search_related, name='directorio'),

    path('sugerencias/', common_views.create_suggestion, name='create_suggestion'),

    path('miperfil/', personal_views.user_profile, name='perfil'),
    path('miperfil/modificar/', personal_views.change_profile_get, name='change_profile_get'),
    path('miperfil/modificar/basico', personal_views.change_profile, name='change_profile'),

    path('miperfil/modificar/telefono', personal_views.change_phone, name='change_phone'),

    re_path(r'^perfil/(?P<ff_id>\d+)/$', personal_views.user_profile, name='perfil_f'),
    re_path(r'^eliminar/telefono/(?P<phone_id>\d+)/$', personal_views.delete_phone, name='delete_phone'),

    re_path(r'^verplanilla/(?P<ff_id>\d+)/$', personal_views.view_cnb_form, name='view_cnb_form'),

    path('servicios/insertar/', ops_views.insert_service, name='insert_service'),
    path('servicios/', ops_views.list_services, name='list_services'),
    path('servicios/exportar/', ops_views.export_services_excel, name='export_services_excel'),
    re_path(r'^servicio/(?P<service_id>\d+)/$', ops_views.view_service, name='view_service'),
    re_path(r'^servicio/(?P<service_id>\d+)/image$', ops_views.service_upload_image, name='service_upload_image'),

    path('comunicaciones/', comunicaciones_views.list_communications, name='list_communications'),
    path('comunicaciones/nueva/', comunicaciones_views.create_communication, name='create_communication'),

    path('arrestos/insertar/', ops_views.insert_arrest, name='insert_arrest'),
    path('arrestos/insertar/pago/', ops_views.insert_arrest_payment, name='insert_arrest_payment'),

    path('personas/autocompletar/', common_views.autocomplete_person, name='autocomplete_person'),
    path('bomberos/autocompletar/', personal_views.autocomplete_firefighter, name='autocomplete_firefighter'),
    path('bomberos/activos/autocompletar/', personal_views.autocomplete_firefighter_active, name='autocomplete_firefighter_active'),
    path('bomberos/sample/', personal_views.ff_sample, name='firefighter_sample'),

    # ADMIN
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
