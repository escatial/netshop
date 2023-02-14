# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Area(models.Model):
    areaid = models.IntegerField(primary_key=True)
    areaname = models.CharField(max_length=50)
    parentid = models.IntegerField()
    arealevel = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'area'


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class GoodsappCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    cname = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'goodsapp_category'


class GoodsappColor(models.Model):
    id = models.BigAutoField(primary_key=True)
    colorname = models.CharField(max_length=10)
    colorurl = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'goodsapp_color'


class GoodsappGoods(models.Model):
    id = models.BigAutoField(primary_key=True)
    gname = models.CharField(max_length=100)
    gdesc = models.CharField(max_length=200)
    oldprice = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(GoodsappCategory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'goodsapp_goods'


class GoodsappGoodsdetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    gdurl = models.CharField(max_length=100)
    detailname = models.ForeignKey('GoodsappGoodsdetailname', models.DO_NOTHING)
    goods = models.ForeignKey(GoodsappGoods, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'goodsapp_goodsdetail'


class GoodsappGoodsdetailname(models.Model):
    id = models.BigAutoField(primary_key=True)
    gdname = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'goodsapp_goodsdetailname'


class GoodsappInventory(models.Model):
    id = models.BigAutoField(primary_key=True)
    count = models.PositiveBigIntegerField()
    color = models.ForeignKey(GoodsappColor, models.DO_NOTHING)
    goods = models.ForeignKey(GoodsappGoods, models.DO_NOTHING)
    size = models.ForeignKey('GoodsappSize', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'goodsapp_inventory'


class GoodsappSize(models.Model):
    id = models.BigAutoField(primary_key=True)
    sname = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'goodsapp_size'

class UserInfo(models.Model):
    """用户信息"""
    uname = models.CharField(max_length=100,verbose_name="用户名",)
    pwd = models.CharField(max_length=100,verbose_name="密码",)

    def __str__(self):
        return self.uname

class Address(models.Model):
    aname = models.CharField(max_length=30)
    aphone = models.CharField(max_length=11)
    addr = models.CharField(max_length=100)
    # 只有一个默认地址
    isdefault = models.BooleanField(default=False)
    userinfo = models.ForeignKey(UserInfo,on_delete=models.CASCADE,)

    def __str__(self):
        return self.aname

