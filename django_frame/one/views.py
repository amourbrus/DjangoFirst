from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse  # 注意导包路径
# Create your views here.
from django.http import HttpResponse
from django.views import View
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet

from one.serializers import BookInfoModelSerializers, BookInfoSerializer
from .models import BookInfo

def index(request):
    # return HttpResponse('hello world')
    return render(request, 'index.html',{'message':'hello'})

"""reverse"""

def say(request):
    url = reverse('one:index')  # 返回 /users/index/

    print(url)
    # return HttpResponse('say')
    return redirect(url)
"""URL路径参数"""
def weather(request, city, year):
    print('city=%s' % city)
    print('year=%s' % year)
    # return HttpResponse('OK python',)
    response = HttpResponse("ok python")
    response.status_code = 300
    # response["Itcast"] = "python"
    return response

def weather2(request, city, year):
    print('city=%s' % city)
    print('year=%s' % year)
    return HttpResponse('OK')

# /qs/?a=1&b=2&a=3

def qs(request):
    a = request.GET.get('a')
    b = request.GET.get('b')
    alist = request.GET.getlist('a')
    print(a)  # 3
    print(b)  # 2
    print(alist)  # ['1', '3']
    return HttpResponse('OK')

# post 请求表单
def get_body(request):
    a = request.POST.get('a')
    b = request.POST.get('b')
    alist = request.POST.getlist('a')
    print(a)  # 3
    print(b)  # 2
    print(alist)  # ["1","3"]
    return HttpResponse('OK')


import json
def get_body_json(requset):
    json_str = requset.body
    print(json_str)    # b'{\n    "a": 1, "b": 2\n}\n\n'
    json_str = json_str.decode()  # py3.6不用
    data = json.loads(json_str)
    print(data)  # {'a': 1, 'b': 2}
    print(data["a"], "and",data["b"])   # 1 and 2
    return HttpResponse("okay")



# 测试中间件的测试函数，下面是零食测试Jsonresponse格式unicode问题
def demo_view(request):
    print('view 视图被调用')
    # return HttpResponse('okay')
    dict1 = {"zhong": "文","hello":"world"}
    book_list = []
    book_list.append(dict1)
    # book_str = json.dumps(book_list)   # json to str
    # book = json.loads(book_list)   # str  to  dict
    # book_list = dict(book_list)
    # return HttpResponse(book_list)
    # JsonResponse的问题：返回列表套字典格式时，中文unicode
    return JsonResponse(book_list,safe=False)

#  set cookie
def cookie(request):
    response = HttpResponse('ok')
    response.set_cookie('itcast1', 'python1')  # 临时cookie
    response.set_cookie('itcast2', 'python2', max_age=3600)  # 有效期一小时
    return response

# get cookie
def cookies(request):
    cookies = request.COOKIES.get("itcast1")
    print(cookies)
    return HttpResponse("ok ok")


"""使用Django开发REST接口,未导入restframe"""
# book & hero little case
# get all books, post(add) books, one url need no id
# get one book,  update one book , delete book , one url


class BooksView(View):
    # 获取全部书籍
    # get  /books
    def get(self,request):
        # 1,获得全部书 --> [{"btitle":"西游记","bpub_date":"1990-8-7"..},{}...]
        # books = BookInfo.objects.all()
        # wrong:type object 'BookInfo' has no attribute 'objects'
        # because it has used class manager,change as below ok
        books = BookInfo.books.all()
        #  <QuerySet [<BookInfo: 射雕英雄传>, <BookInfo: 天龙八部>,
        #  <BookInfo: 笑傲江湖>, <BookInfo: 雪山飞狐>, <BookInfo: hello>,
        # <BookInfo: hello>, <BookInfo: ssss>, <BookInfo: 三国演义（第二版）>,
        # <BookInfo: 三国shuihu）>]>

        # 2,数据换格式, serializer
        book_list = []
        for book in books:
            book_list.append({
                "id":book.id,
                "btitle":book.btitle,
                "bpub_date":book.bpub_date,
                "bread":book.bread,
                "bcomment":book.bcomment,
                "image":book.image.url if book.image else ""
            })
        # 3, show books, JsonResponse :By default only ``dict`` objects
      # are allowed to be passed due to a security
        return JsonResponse(book_list,safe=False)

    # 增加书籍
    # post /books
    def post(self, request):
        """add book"""
        # 1,get data from web_font
        body_data = request.body
        print("body data =====",type(body_data))  # <class 'bytes'>
        # 2,decode
        str_data = body_data.decode()  # <class 'str'>
        print("str_data", type(str_data))
        # loads ->  str to dict
        data = json.loads(str_data)   # <class 'dict'>
        print("data ====", type(data))

        # 4, write into database
        book = BookInfo.books.create(
            btitle = data["btitle"],
            bpub_date = data["bpub_date"]
        )
        # 5, show data
        return JsonResponse({
            "id":book.id,
            "btitle": book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'image': book.image.url if book.image else ''
        })

class BookView(View):
    # get /books/3
    def get(self,request, id):  # request cannot gone,must have,
        # or bug get() got multiple values for argument 'id'
        """get one book"""

        # 1,query database , if exists or not
        # 2,show data and return
        try:
            book = BookInfo.books.get(id=id)
        except Exception as e:
            raise e
        print("type book is", type(book))
        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'image': book.image.url if book.image else ''
        })

    def put(self, req, id):
        """update one book"""
        # 1,query database, if exist or not
        try:
            book = BookInfo.books.get(id=id)
        except Exception as e:
            raise e
        # 2, get data from web font, json
        body_data = req.body   # type <class 'bytes'>
        print("body_data type",type(body_data))
        # 3, decode
        data_str = body_data.decode()
        data = json.loads(data_str)  # <class 'dict'>
        print("data type", type(data))
        # 4, update data
        book.btitle = data['btitle']
        book.bpub_date = data['bpub_date']
        book.save()
        # 5, show data
        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'image': book.image.url if book.image else ''
        })

    def delete(self, request, id):
        # 1, query , if exist or not
        # 2, delete()
        try:
            book = BookInfo.books.get(id=id)
        except Exception as e:
            raise e

        book.delete()
        return HttpResponse("delete success")


"""use DRF  见识DRF的魅力 """
class BooksViewSet(ModelViewSet):
    # get data
    queryset = BookInfo.books.all()
    # show data , create a serializer before
    serializer_class = BookInfoModelSerializers

"""views """
# APIView
# class BookInfoView(APIView):
#     # 获取全部书籍，进行序列化并返回
#     def get(self,request):
#         # 1,query database
#         # books = BookInfo.objects.all()
#         books = BookInfo.books.all()
#         # 2, format change  --> serializer
#         # serializer = BookInfoModelSerializers(books,many=True)
#         serializer = BookInfoSerializer(books,many=True)  # wrong: TypeError at /one/apiview/
# # <django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager.<locals>.RelatedManager object at 0x7f6384513550> is not JSON serializable
#         # comment or remove the "heroinfo_set = serializers.PrimaryKeyRelatedField" in the BookInfoSerializer
#         # 3,return
#         # return Response(serializer)   # wrong:TypeError ..is not JSON serializable
#         return Response(serializer.data)
#
#
#     def post(self, request):
#         # 1,get the data from front
#         # body_data = request.data
#         # str_data = body_data.decode()
#         # data = json.loads(str_data)
#         # request 是DRF封装好的类字典的
#         ser = BookInfoSerializer( data = request.data)
#         ser.is_valid(raise_exception=True)
#         ser.save()
#
#         return Response(ser.data)


# # GenericAPIView
# class BookInfoView(GenericAPIView):
#     serializer_class = BookInfoSerializer
#     queryset = BookInfo.books.all()
#
#     def get(self,request):
#         books = self.get_queryset()
#         ser = BookInfoSerializer(books, many=True)
#         return Response(ser.data)


# ListModelMixin, GenericAPIView
# CreateModelMixin   for post
# class BookInfoView(ListModelMixin, GenericAPIView,CreateModelMixin):
#     serializer_class = BookInfoSerializer
#     queryset = BookInfo.books.all()
#
#     def get(self,request):
#         # get all books
#         return self.list(request)
#
#     def post(self,request):
#         # add one book
#         return self.create(request)

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2  # 每页数目
    page_size_query_param = "page_size"
    max_page_size = 5

# ListAPIView, CreateAPIView
class BookInfoView(ListAPIView, CreateAPIView):
    serializer_class = BookInfoSerializer
    queryset = BookInfo.books.all()

    filter_backends = [OrderingFilter]
    ordering_fields = ("id", "bread")

    pagination_class = LargeResultsSetPagination

# GenericAPIView
# class BookDetailView(GenericAPIView):
#     serializer_class = BookInfoSerializer
#     queryset = BookInfo.books.all()
#
#     def get(self,request,pk):
#         # 获取一本书的数据
#         book = self.get_object()
#         # 序列化
#         ser = BookInfoSerializer(book)
#         return Response(ser.data)


class BookDetailView(RetrieveModelMixin,GenericAPIView):
    # GenericAPIView  gave below two
    serializer_class = BookInfoSerializer
    queryset = BookInfo.books.all()

    def get(self,req,pk):
        return self.retrieve(req)


# 视图集使用
# ViewSet  vs APIView
# class BooksInfoViewSet(ViewSet):
#     def list(self, request):
#         book = BookInfo.books.all()
#         ser = BookInfoSerializer(book,many=True)
#         return Response(ser.data)
#
#     def retrieve(self, request, pk):  # retrieve
#         try:
#             # book = BookInfo.books.all()  # AttributeError 'QuerySet' object has no attribute 'btitle'
#             book = BookInfo.books.get(id=pk)
#         except BookInfo.DoesNotExist:
#             return Response("data does not exist")
#
#         serializer = BookInfoSerializer(book)
#         return Response(serializer.data)


# 自定义动作
class BookInfoViewSet(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    queryset = BookInfo.books.all()
    serializer_class = BookInfoSerializer

    @action(methods=['get'],detail=False)
    def latest_d(self,request):
        # 返回最新的图书信息
        book = BookInfo.books.latest("id")
        ser = self.get_serializer(book)
        return Response(ser.data)


    @action(methods=['put'],detail=True)
    def read_d(self,req, pk):
        # 修改图书的阅读量数据
        book = self.get_object()
        book.bread = req.data.get('bread')  # ziliao wrong
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)










