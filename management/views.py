from django.shortcuts import render
from django.views.decorators.http import require_http_methods


# Create your views here.
@require_http_methods(["GET"])
def home(request):
    return render(request, "home.html")
