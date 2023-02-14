from django.shortcuts import render,HttpResponse
from goodsapp.models import *
from django.core.paginator import Paginator
from netshop import settings

# Create your views here.
def index(request,categoryid=2,page_num=1):
    """商品列表页"""
    # 1. 获取所有分类
    categoryList = Category.objects.all().order_by("id")
    # 2. 获取当前分类下的所有商品
    goodsList = Goods.objects.filter(category_id=categoryid)

    # 添加分页
    paginator = Paginator(object_list=goodsList,per_page= settings.PER_PAGE_NUMBER)
    # 获取当前页的数据
    goods_page = paginator.get_page(page_num)

    # 设置传递参数
    context = {
        "categoryList":categoryList,
        "currcategoryid":categoryid,
        "goods_page":goods_page,
        # page_num 当前页 paginator.num_pages总共有多少页
        "page_range":get_page_range_by_page_and_max_page(page_num,paginator.num_pages,)
    }
    return render(request,"goodsapp/index.html",context= context)

# 分页栏
def get_page_range_by_page_and_max_page(page,max_page,num=10):
    min = page - int(num/2)
    min = min if min > 1 else 1
    max = min + num - 1
    max=max if max < max_page else max_page
    return range(min,max+1)
def recommend(func):
    def inner(request,goodsid,*args,**kwargs):
        # 浏览商品id
        c_goodsIdList = request.COOKIES.get("recommend_goodsid","")

        # 将由空格拼接的字符串转化为列表
        goodsIdList = [id for id in c_goodsIdList.split() if id.strip()]

        # 判断当前浏览的商品是否在浏览列表中，如果存在，先删除， 再将最近浏览的商品插入列表第一位置
        if str(goodsid) in goodsIdList:
            goodsIdList.remove(str(goodsid))
        goodsIdList.insert(0,goodsid)

        # 根据推荐商品id获取商品信息
        goodsObjectList = [Goods.objects.get(id=gid) for gid in goodsIdList if gid != goodsid and Goods.objects.get(id=gid).category.id==Goods.objects.get(id=goodsid).category.id][:4]

        # 使用cookie保存商品id浏览记录
        # 获取response对象
        response = func(request,goodsid,recommend_list=goodsObjectList,*args,**kwargs)
        # 获取cookie
        response.set_cookie("recommend_goodsid"," ".join([str(id) for id in goodsIdList]),max_age=3*24*3600)
        return response
    return inner


@recommend
def goodsdetail(request,goodsid,recommend_list=[]):
    """根据商品id获取商品详情"""
    try:
        goods = Goods.objects.get(id=goodsid)
        context = {
            "goods":goods,
            "recommend_list":recommend_list
        }
        return render(request,"goodsapp/goodsdetail.html",context=context)
    except Goods.DoesNotExist:
        return HttpResponse(status=404)