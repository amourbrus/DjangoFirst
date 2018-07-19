from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from rest_framework.viewsets import ModelViewSet

from booktest.models import BookInfo
from booktest.serializers import BookInfoSerializer

import json
"""编写视图　　ModelViewSet 　BookInfo"""
class BookInfoViewSet(ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer


"""rest 规范接口 业务需求　获取所有的图书,　获取一本图书"""




class BooksAPIView(View):
    """"查询所有图书
    路由　GET  /bookall"""
    def get(self, request):
        queryset = BookInfo.objects.all()  # 查询所有的图书，获取数据
        book_list = []  # 做序列化, 成为前端需要的数据格式
        for book in queryset:
            book_list.append({
                'id': book.id,
                'btitle': book.btitle,
                'bpub_date': book.bpub_date,
                'bread': book.bread,
                'bcomment': book.bcomment,
            })
        # 前端默认只接收json 的格式，　若现在传的列表，则要加safe=False
        # 看JsonResponse　代码　'In order to allow non-dict objects to be serialized set the '
        #         'safe parameter to False.'
        return JsonResponse(book_list, safe=False)

    def post(self, request):
        """新增图书　路由　POST / bookall"""
        json_bytes = request.body
        json_str = json_bytes.decode()
        # book_dict = json.loads(json_str)
        book_dict = json.dumps(json_str)

        book = BookInfo.objects.create(
            btitle = book_dict.get('btitle'),
            bpub_date = book_dict['bpub_date']
        )
        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'image': book.image.url if book.image else ''
        })


class bkAPIView(View):
    def get(self, request, pk):
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
        })

    def put(self,request,id):
        """修改图书信息"""
        try:
            book = BookInfo.objects.get(id=id)
        except Exception as e:
            raise e
        # 获取前端传来的数据
        body_data = request.body
        # 转码
        str_data = body_data.decode()
        data = json.loads(str_data)
        # 修改数据
        book.btitle = data['btitle']
        book.bpub_date = data['bpub_data']
        book.save()

        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
        })

    def delete(self, request, id):
        try:
            book = BookInfo.objects.get(id=id)

        except Exception as e:
            raise e

        book.delete()

        return HttpResponse('ok')


