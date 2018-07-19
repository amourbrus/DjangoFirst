from django.shortcuts import render
from .models import BookInfo
from django.http import HttpResponse
# Create your views here.

def index(request):
    # return HttpResponse("hello world")
    data = {
        "message":"hello world 哈哈哈哈哈"
    }
    return render(request, 'index.html',data)

