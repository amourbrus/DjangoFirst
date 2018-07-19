from django.contrib import admin
from users.models import BookInfo
# Register your models here.

# admin.site.register(BookInfo)

# 方式二 装饰器
@admin.register(BookInfo)
class BookInfoAdmin(admin.ModelAdmin):

    list_per_page = 5  # 页大小默认每页显示１０条数据
    actions_on_top = True  # 操作选项的位置
    actions_on_bottom = True
    list_display = ['id', 'btitle','bread','bpub_date']  # 列表中的列－－－字段
    # list_filter = ['btitle', 'bread']
    admin.site.site_header = '传智书城'
    admin.site.site_title = '传智书城MIS'
    admin.site.index_title = '欢迎使用传智书城MIS'
# 注册的两种方式、
# admin.site.register(BookInfo, BookInfoAdmin)


