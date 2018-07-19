from django.contrib import admin

# Register your models here.
from one.models import BookInfo, HeroInfo
# 站点管理，　定义站点管理类，注册该类，写元素，需要用到模型类的定义方法即可调用
# 定义管理类
class BookInfoAdmin(admin.ModelAdmin):
    list_per_page = 3
    list_display = ['id','btitle','bpub_date']

class HeroInfoAdmin(admin.ModelAdmin):
    list_display = ['id','hname','hbook','read']
    list_filter = ['hbook', 'hgender']
    search_fields = ['hname']
# 使用管理类的两种方式
# ways 1
admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo,HeroInfoAdmin)
# ways2  装饰器
# @admin.register(BookInfo)
# class BookInfoAdmin(admin.ModelAdmin):
#     pass


