from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'say/$', views.say),
    # 路由使用分组括号形式
    # url(r'^weather/(\w+)/(\d+)/$', views.weather),
    url(r'weather/(?P<city>\w+)/(?P<year>\d+)$', views.weather),
    url(r'qs', views.qs),
    url(r'getbody', views.getBody),
    url(r"getjson/$", views.get_body_json),
    url(r"header", views.get_headers),
    url(r"demo", views.demo_view),

]

