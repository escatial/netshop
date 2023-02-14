from django.shortcuts import render,redirect,HttpResponse
import jsonpickle
from utils.cartmanager import *
from utils.alipay_p3 import AliPay
import uuid
from orderapp.models import *
from datetime import datetime
from userapp.models import *
from goodsapp.models import *
from django.db.models import F


# Create your views here.
def toOrder(request):
    """结算视图"""
    # 获取参数
    cartitems = request.GET.get("cartitems","")
    totalPrice = request.GET.get("totalPrice",0)
    # 判断用户是否登录
    # 从session对象中获取用户信息
    # 如果没有登录
    if not request.session.get("user",""):
        return render(request,"userapp/login.html",{"reflag":"orderapp","cartitems":cartitems,"totalPrice":totalPrice})
    # 获取登录用户信息
    user = jsonpickle.loads(request.session.get("user")) 
    # 根据用户获取地址信息
    addrObj = user.address_set.get(isdefault=True)

    # 获取订单中商品信息
    cartitemList = jsonpickle.loads(cartitems)
    # print(cartitemList)cartItemObjList
    # 循环遍历cartitemList生成cartItem对象列表
    # 创建DBCartManager实例对象
    dbCartObj = DBCartManger(user)
    cartItemObjList = [dbCartObj.get_cartitems(**item) for item in cartitemList if item]

    context = {
        "addrObj":addrObj,
        "cartItemObjList":cartItemObjList,
        "totalPrice":totalPrice,
    }
    return render(request,"orderapp/toOrder.html",context=context)

alipay = AliPay(
    appid="2021000122601431", 
    app_notify_url="http://127.0.0.1:8000/orderapp/checkpay/", 
    app_private_key_path="keys/my_private_key.txt",
    alipay_public_key_path="keys/alipay_public_key.txt", 
    return_url="http://127.0.0.1:8000/orderapp/checkpay/", 
    debug=True)

def toPay(request):

    # 获取支付金额
    totalPrice = request.GET.get("totalPrice",0)
    # 获取请求参数
    # 保存订单
    orderObj = Order.objects.create(
        out_trade_num = uuid.uuid4().hex,
        order_num = datetime.strftime(datetime.now(),"%Y%m%d%H%M%S"),
        payway= request.GET.get("payway",""),
        address = Address.objects.get(id=request.GET.get("address","")),
        user = jsonpickle.loads(request.session.get("user")),
    )
    # 保存订单项
    cartitems = jsonpickle.loads(request.GET.get("cartitems","")) 
    # cartitems [{"goodsid":3,"colorid":2,"sizeid":1,"count":3},{"goodsid":3,"colorid":2,"sizeid":1,"count":3},] 
    orderItemList = [OrderItem.objects.create(order = orderObj,**ci) for ci in cartitems if ci]

    # 创建Alipay实例对象
    # 调用支付界面
    params = alipay.direct_pay(subject="京东商城", out_trade_no=orderObj.out_trade_num, total_amount=totalPrice,)
    return redirect(alipay.gateway+"?"+params)
def checkPay(request):
    # 获取请求参数
    params = request.GET.dict()
    # 获取sign
    sign = params.pop("sign")
    # 判断是否支付成功
    if alipay.verify(params,sign):
        # 1.修改订单状态，以及trade_no设置值
        orderObj = Order.objects.get(out_trade_num = params.get("out_trade_no",""))
        orderObj.status = "待发货"
        orderObj.trade_no = params.get("trade_no")
        # 2.修改库存
        # 根据订单获取订单项
        orderitems = orderObj.orderitem_set.all()
        [Inventory.objects.filter(goods_id=oi.goodsid,color_id=oi.colorid,size_id=oi.sizeid).update(count=F("count")-oi.count) for oi in orderitems]
        # 3.修改购物车中的数据
        # 获取当前用户
        user =jsonpickle.loads(request.session.get("user")) 
        [user.cartitem_set.filter(goodsid=oi.goodsid,colorid=oi.colorid,sizeid=oi.sizeid).delete() for oi in orderitems]

        return HttpResponse("支付成功")
    else:
        return HttpResponse("支付失败")