from django.db import models

# Create your models here.
class Category(models.Model):
    """商品分类"""
    cname = models.CharField(max_length=30,verbose_name="产品分类名称")

    def __str__(self):
        return self.cname

class Goods(models.Model):
    """商品表"""
    gname = models.CharField(max_length=100,verbose_name="商品名称")
    gdesc = models.CharField(max_length=200,verbose_name="商品描述")
    # max_digits=5总共5位数,decimal_places=2小数两位
    oldprice = models.DecimalField(max_digits=5,decimal_places=2,verbose_name="商品原价")
    price = models.DecimalField(max_digits=5,decimal_places=2,verbose_name="商品现价")
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    # 获取商品图片
    def get_img_url(self):
        return self.inventory_set.first().color.colorurl

    # 获取颜色
    def get_colors(self):
        colors = []
        for inventory in self.inventory_set.all():
            color = inventory.color
            # 去重
            if color not in colors:
                colors.append(color)
        return colors
    # 获取尺寸
    def get_size(self):
        sizes = set()
        for inventory in self.inventory_set.all():
            sizes.add(inventory.size)
        return sizes

    # 存储结构：{”参数规格“：["url"],"整体款式"：["url"],"模特实拍":["url1","url2","url3"...]}
    def getDetailInfo(self):
        # 存储数据
        datas = {}
        # 根据商品获取商品详情
        for detail in self.goodsdetail_set.all():
            # 根据商品详情获取商品详情名称
            detailName = detail.detailname.gdname
            # 判断数据中是否已经存在detailName
            if detailName in datas:
                datas[detailName].append(detail.gdurl)
            else:
                datas[detailName] = [detail.gdurl]
        return datas

    def __str__(self):
        return self.gname

class GoodsDetailName(models.Model):
    """商品详情名称"""
    gdname = models.CharField(max_length=30,verbose_name="商品详情名称")

    def __str__(self):
        return self.gdname

class GoodsDetail(models.Model):
    """商品详情表"""
    gdurl = models.ImageField(verbose_name="详情图片路径",upload_to="")
    detailname = models.ForeignKey(GoodsDetailName,verbose_name="商品详情名称",on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE)

class Size(models.Model):
    "商品尺寸"
    sname = models.CharField(max_length=20,verbose_name="商品尺寸名称")

class Color(models.Model):
    """商品颜色"""
    colorname = models.CharField(max_length=10,verbose_name="商品颜色名称")
    colorurl = models.ImageField(verbose_name="颜色保存路径",upload_to="color/")

class Inventory(models.Model):
    """商品库存"""
    count = models.PositiveBigIntegerField(verbose_name="库存数量",)
    size = models.ForeignKey(Size,verbose_name="商品尺寸",on_delete=models.CASCADE)
    color = models.ForeignKey(Color,verbose_name="商品颜色",on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE,verbose_name="所属商品")