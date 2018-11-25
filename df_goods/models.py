from django.db import models

# Create your models here.
# 商品分类
class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

# 商品
from tinymce.models import HTMLField
class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    # 图片位置
    gpic = models.ImageField(upload_to='df_goods')
    # 价格：decimal_places=2：小数点后2位
    gprice = models.DecimalField(max_digits=5, decimal_places=2)
    isDelete = models.BooleanField(default=False)
    # 单位
    gunit = models.CharField(max_length=20, default='500g')
    # 人气：点击量排序
    gclick = models.IntegerField()
    # 简介
    gjianjie = models.CharField(max_length=200)
    # 库存
    gkucun = models.IntegerField()
    # 商品详情：HTMLField：富文本编辑器
    gcontent = HTMLField()
    # 外键
    gtype = models.ForeignKey('TypeInfo', on_delete=models.CASCADE)
    # 广告推荐
    # gadv = models.BooleanField(default=False)