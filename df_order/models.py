from django.db import models

# Create your models here.

# 订单的主表
class OrderInfo(models.Model):
    # 订单编号
    oid = models.CharField(max_length=20,primary_key=True)
    # 某个用户的订单
    user = models.ForeignKey('df_user.UserInfo', on_delete=models.CASCADE)
    # 订单日期
    odate = models.DateTimeField(auto_now=True)
    # 是否支付
    oIsPay = models.IntegerField(default=0)
    # 总金额（最大金额：4位整数，两位小数：9999.99）
    ototal = models.DecimalField(max_digits=6,decimal_places=2)
    # 订单地址
    oaddress = models.CharField(max_length=150,default='')
    # 支付方式
    zhifu = models.IntegerField(default=0)

# 订单的详细表
class OrderDetailInfo(models.Model):
    # 商品
    goods=models.ForeignKey('df_goods.GoodsInfo', on_delete=models.CASCADE)
    # 关联订单表
    order=models.ForeignKey(OrderInfo, on_delete=models.CASCADE)
    # 价格
    price=models.DecimalField(max_digits=5,decimal_places=2)
    # 数量
    count=models.IntegerField()