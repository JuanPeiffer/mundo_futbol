from django.http import HttpResponse

# Create your views here.
def hola(request):
    return HttpResponse("Hola mundo")
def about(request):
    return HttpResponse("Sobre mundo")