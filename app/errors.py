from django.http import HttpResponse

def error405(code):
    return HttpResponse("ERROR 405")