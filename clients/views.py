from django.shortcuts import render
from .models import Client

def clients_page(request):
    clients = Client.objects.all()
    return render(request, 'clients/list.html', {
    'clients': clients
})