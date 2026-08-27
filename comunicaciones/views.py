#coding=utf-8
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from comunicaciones.models import Communication


class CommunicationForm(forms.ModelForm):
    class Meta:
        model = Communication
        fields = ['title', 'body', 'pinned']
        labels = {
            'title': 'Título',
            'body': 'Contenido',
            'pinned': 'Fijar como importante',
        }


@login_required
def list_communications(request):
    communications = Communication.objects.all()
    return render(request, "list_communications.html", {"communications": communications})


@login_required
def create_communication(request):
    if request.method == 'POST':
        form = CommunicationForm(request.POST)
        if form.is_valid():
            communication = form.save(commit=False)
            try:
                communication.created_by = request.user.firefighter
            except Exception:
                pass
            communication.save()
            messages.success(request, u'La comunicación fue publicada exitosamente')
            return redirect('list_communications')
    else:
        form = CommunicationForm()
    return render(request, "create_communication.html", {"form": form})
