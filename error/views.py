from django.shortcuts import render, render_to_response
import time

# Create your views here.
def page_not_found(request):

    return render(request, '404.html')


def server_Error(request):
    return render_to_response('500.html')
