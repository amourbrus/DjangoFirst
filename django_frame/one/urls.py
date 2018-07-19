from django.conf.urls import url

from . import views

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r"rdf", views.BooksViewSet)

router_1 = DefaultRouter()
router_1.register(r"read", views.BookInfoViewSet, base_name="def_read")

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^say', views.say, name='say'),
    url(r'^weather/([a-z]+)/(\d{1})/$', views.weather),
    url(r'demo', views.demo_view),
    url(r'^weather2/(?P<city>[a-z]+)/(?P<year>\d{4})/$', views.weather2),
    url(r"qs/$",views.qs),
    url(r"body/$",views.get_body),
    url(r"bodys/$", views.get_body_json),
    url(r"cookie/$", views.cookie),
    url(r"cookies/$", views.cookies),
    url(r"books/$", views.BooksView.as_view()),
    url(r"books/(?P<id>\d+)/$",views.BookView.as_view()),
    # APIView
    url(r"infoview/$",views.BookInfoView.as_view()),
# GenericApiVIew
    url(r'genbook/(?P<pk>\d+)/$', views.BookDetailView.as_view()),
    # url(r'genbooks/(?P<pk>\d+)/$', views.HeroInfoDetail.as_view(), name='books-detail')
    # 视图集
    # url(r'^viewset/$', views.BooksInfoViewSet.as_view({'get':'list'})),
    # url(r"^retri/(?P<pk>\d+)$", views.BooksInfoViewSet.as_view({'get':"retrieve"})),
    url(r"^latest/$",views.BookInfoViewSet.as_view({'get':"latest_d"})),
    # url(r"^reads/$", views.BookInfoViewSet.as_view({"put":"read_d"}))
]

urlpatterns += router.urls
urlpatterns += router_1.urls


