from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponseBadRequest
from utils.cartmanager import*

# Create your views here.
def cartview(request):
    # 在session中存取数据使用多级字典需要实时更新
    request.session.modified = True
    """购物车"""
    # 获取表单数据
    # 1. 获取购物操作
    flag = request.POST.get("flag")
    dbCartMangerObj = getCartManger(request)
    if flag == "add":
        # 加入购物车
        dbCartMangerObj.add(**request.POST.dict())
    elif flag == "plus":
        """增加商品数量"""
        dbCartMangerObj.update(step=1,**request.POST.dict())
    elif flag == "minus":
        dbCartMangerObj.update(step=-1,**request.POST.dict())
    elif flag == "delete":
        dbCartMangerObj.delete(**request.POST.dict())
    return redirect("/cartapp/queryAll/")
def queryAll(request):
    """查询购物车方法"""
    dbCartMangerObj =   getCartManger(request)
    cartitemlist = dbCartMangerObj.queryAll()
    context = {
        "cartitemlist":cartitemlist,
    }
    return render(request,"cartapp/cart.html",context=context)