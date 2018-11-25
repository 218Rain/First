from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.


class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttitle']
class GoodsInfoAdmin(admin.ModelAdmin):
    # 分页
    list_per_page = 15
    # 过滤字段
    list_display = ['id', 'gtitle', 'gprice', 'gunit', 'gkucun', 'gcontent', 'gtype']

# 注册模型类
admin.site.register(TypeInfo,TypeInfoAdmin)
admin.site.register(GoodsInfo,GoodsInfoAdmin)


