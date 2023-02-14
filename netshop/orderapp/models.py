from django.db import models
from userapp.models import *

# Create your models here.
class Order(models.Model):
    """订单模块"""
    out_trade_num = models.UUIDField()
    trade_no = models.CharField(max_length=120)
    order_num = models.CharField(max_length=100)
    status = models.CharField(max_length=20,default="待支付")
    payway = models.CharField(max_length=20,default="alipay")
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE)

class OrderItem(models.Model):
    """订单模型"""
    goodsid = models.PositiveBigIntegerField()
    colorid = models.PositiveBigIntegerField()
    sizeid = models.PositiveBigIntegerField()
    count = models.PositiveBigIntegerField()
    order = models.ForeignKey(Order,on_delete=models.CASCADE)