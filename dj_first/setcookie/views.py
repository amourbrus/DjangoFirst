from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


# todo 设置cookie ，设置完成后在 demo_view2中get 查看
# todo urls.py  --> url(r'set/$', views.demo_view),
from django.template import loader


def demo_view(request):
    response = HttpResponse('ok')
    response.set_cookie('itcast1', 'python1')  # 临时cookie
    response.set_cookie('itcast2', 'python2', max_age=3600)  # 有效期一小时
    return response


def demo_view2(request):
    cookie1 = request.COOKIES.get('itcast1')
    cookie2 = request.COOKIES.get('itcast2')
    print("这是cookie 啊",  cookie1)
    print("这是cookie 啊",  cookie2)
    request.session['heng']='hengha'
    session = request.session.get('heng')
    print('这是session啊啊',session)
    return HttpResponse('OK')


from django.views.generic import View

# todo 类视图　　　urls.py　　--> url(r'^register/$', views.RegisterView.as_view())
# 需要继承自　 generic  的　View
# class RegisterView(View):
#     def get(self, request):
#         return render(request, 'register.html')
#
#     def post(self, request):
#         return HttpResponse("这里实习那注册逻辑")


# todo 类装饰器 第一种  urls.py(讲义有错)  --> url(r'^demo/$', views.my_decorator(views.DemoView.as_view()))
def my_decorator(func):
    def wrapper(request, *args, **kwargs):
        print("自定义装饰器被调用了")
        print('请求路径', request.path)
        return func(request, *args, **kwargs)
    return wrapper

# todo 第二种方法　注意这种方法，urls 要恢复类视图写法

from django.utils.decorators import method_decorator

@method_decorator(my_decorator, name='dispatch')    # dispatch 　给所有方法加装饰，换为get 则只给get加，
class DemoView(View):
    # @method_decorator(my_decorator)
    def get(self, request):  # 或者单独在这加，　也是一个方法加
        print("get ways ~~~~")
        return HttpResponse("ok ok get")

    def post(self, request):
        print("post ways")
        return HttpResponse("ok ok post!")

# todo 类视图Mixin　扩展类　　扩展的父类名称通常以Mixin结尾
class ListModelMixin(object):
    """
    list扩展类
    """
    def list(self, request, *args, **kwargs):
        pass

class CreateModelMixin(object):
    """
    create扩展类
    """
    def create(self, request, *args, **kwargs):
        pass


class BooksView(CreateModelMixin, ListModelMixin, View):
    """
    同时继承两个扩展类，复用list和create方法
    """
    def get(self, request):
        self.list(request)
        pass

    def post(self, request):
        self.create(request)
        pass

class SaveOrderView(CreateModelMixin, View):
    """
    继承CreateModelMixin扩展类，复用create方法
    """
    def post(self, request):
        self.create(request)
        pass


# todo 定义中间件工厂函数---在应用目录建一个middleware文件,里面写中间件函数
# def simple_middleware(get_response):
#     # 此处编写的代码仅在Django第一次配置和初始化的时候执行一次。
#
#     def middleware(request):
#         # 此处编写的代码会在每个请求处理视图前被调用。
#
#         response = get_response(request)
#
#         # 此处编写的代码会在每个请求处理视图之后被调用。
#
#         return response
#
#     return middleware


# todo 定义测试函数, urls.py add url -->url(r'test/$', views.testing_mid),
def testing_mid(request):
    print("view has been quoted")
    return HttpResponse("ok okay,ditch")

# 模板加载的原理  --　注册路由，　虽然可以直接／static／　访问到静态文件，但那是没有数据的哦
def index(request):
    template = loader.get_template('index.html')
    context = {'city':"北京　北京"}
    return HttpResponse(template.render(context))
