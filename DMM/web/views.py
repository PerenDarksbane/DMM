from django.shortcuts import render

import requests as r

# Create your views here.
def index(request):
    return render(request, 'index.html')
