from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'set/$', views.demo_view),  # 写这些时函数要去掉括号－－tab 会有
    url(r'^get/$', views.demo_view2),
    # url(r'^register/$', views.RegisterView.as_view()),
    # url(r'demo/$', views.my_decorator(views.DemoView.as_view()))
    url(r'demo/$', views.DemoView.as_view()),  # as_view() 括号
    url(r'test/$', views.testing_mid),
    url(r'index', views.index),
]



