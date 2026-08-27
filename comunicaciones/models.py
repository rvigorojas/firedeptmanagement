#coding=utf-8
from django.db import models
from personal.models import Firefighter


class Communication(models.Model):
    """
    Módulo de "Comunicaciones": tablón de anuncios interno del cuerpo de
    bomberos. Agregado a partir de la retroalimentación de evaluación del
    proyecto, que señaló que esta sección existía en la interfaz pero
    estaba vacía / sin implementar. Ver docs/CORRECCIONES.md.
    """

    class Meta:
        verbose_name = "Comunicación"
        verbose_name_plural = "Comunicaciones"
        ordering = ['-pinned', '-created_at']

    title = models.CharField(max_length=200, verbose_name="Título")
    body = models.TextField(verbose_name="Contenido")
    created_by = models.ForeignKey(
        Firefighter, on_delete=models.CASCADE, related_name='communications',
        verbose_name="Publicado por", null=True, blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de publicación")
    pinned = models.BooleanField(default=False, verbose_name="Fijada (importante)")

    def __str__(self):
        return self.title
