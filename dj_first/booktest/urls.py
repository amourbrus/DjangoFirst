from django.conf.urls import url

from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
url(r'bookall/$', views.BooksAPIView.as_view()),
url(r'bk/$', views.bkAPIView.as_view())
]
router = DefaultRouter()
router.register(r'book', views.BookInfoViewSet)   # 类也是这样，不用as_view
urlpatterns += router.urls   # 列表相加
