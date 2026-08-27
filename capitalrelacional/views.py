#coding=utf-8
#from haystack.query import SearchQuerySet
from capitalrelacional.models import RelationalCompany, RelationalPerson
from django.shortcuts import render
from personal.models import Firefighter
from django.contrib.auth.decorators import login_required

@login_required
def search_related(request):
    query = request.GET.get('query', '')
    data = {"Firefighter": Firefighter.search(query), "RelationalCompany":RelationalCompany.search(query), "query":query}
    return render(request, "directorio.html", data)
