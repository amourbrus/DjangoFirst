from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
import json
# Create your views here.
from django.views import View


def say(request):  # request
    return HttpResponse("hello world")


def weather(request,city,year):
    print('city=%s' % city)
    print('year=%s' % year)

    return HttpResponse('ok')

# 字符串
# /qs/?a=1&b=2&a=3
def qs(request):
    a = request.GET.get('a')
    b = request.GET.get('b')
    alist = request.GET.getlist('a')
    print(a)  #  3
    print(b)   # 2
    print(alist)
    return HttpResponse('ok')  # ['1','3']


# 表单类型数据提交 --- postman　　request.POST.get()
def getBody(request):
    # a = 2435, b=hello, a= world
    a = request.POST.get('a')
    b = request.POST.get('b')
    alist = request.POST.getlist('a')
    print(a)  # world
    print(b)  # hello
    print(alist)    # ['2435', 'world']
    return HttpResponse("ok  ok   ok")


# 非表单类型  -- json  , request.body return  byters类型
# {"a":1,"b":2}


def get_body_json(request):
    json_str = request.body
    print(json_str,"1-1--->", type(json_str))
    # b'{\n"a": 1,\n"b": 2,\n}' 1-1---> <class 'bytes'>
    json_str = json_str.decode()   # py3.6　no need
    print(json_str, "2-2--->", type(json_str))
    # """{
    #     "a": 1,
    #     "b": 2,
    #     } 2-2---> <class 'str'>
    # """

    data = json.loads(json_str)   # json > dict
    print("data >>>",data,"\na>",data["a"],data['b'], type(data))
    # {'a': 1, 'b': 2} 1 2 <class 'dict'>
    return HttpResponse("ok ok double time")

# 请求头
def get_headers(req):
    print(req.META["CONTENT_TYPE"])
    print(req.META)
    print(req.method)    # POST
    print(req.encoding)  # UTF-8
    print(req.path)    # /header  不包含域名和参数
    print(req.user)  # AnonymousUser
    # return HttpResponse(req.META)  # content
    return HttpResponse("ok")


# response
def demo_view(req):
    # return HttpResponse('itcast python', status=400)

    # response = HttpResponse("itcast")
    # response.status_code = 4000
    # response["itcast"] = "python"
    # return response

    return JsonResponse({'city': 'beijing','subject':'python'})