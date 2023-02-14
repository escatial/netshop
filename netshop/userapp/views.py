from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.views import View
from userapp.models import *
import jsonpickle
from captcha.image import ImageCaptcha
from utils.code import gene_text
from utils.cartmanager import *
from django.core import serializers



# Create your views here.
class Register(View):
    """注册视图类"""
    def get(self,request):
        # 跳转到注册页面
        return render(request,"userapp/register.html")

    def post(self,request):
        """完成注册"""
        # 1. 获取表单数据
        uname = request.POST.get("account","")# 如果查询到则返回account，没查询到则返回空
        pwd = request.POST.get("password","")

        # 2. 查询数据库是否已经有该用户
        try:
            user = UserInfo.objects.get(uname=uname,pwd=pwd)
            context = {
                "info":"该账号已注册过"
            }
            return render(request,"userapp/register.html",context=context)
        except UserInfo.DoesNotExist:
            user = UserInfo.objects.create(uname = uname, pwd = pwd)
            # 将用户信息存储到session
            request.session["user"] = jsonpickle.dumps(user)    # 将对象序列化字符串
        return redirect("/userapp/center/")   # 用户中心
        # return HttpResponse("成功")

def userCenter(request):
    """用户中心"""
    return render(request,"userapp/center.html")

class LoginView(View):
    def get(self,request):
        # 获取请求参数
        reflag = request.GET.get("reflag","")
        return render(request,"userapp/login.html",{"reflag":reflag})
    
    def post(self,request):
        # 1. 获取请求参数
        uname = request.POST.get("account","")
        pwd = request.POST.get("password","")
        reflag = request.POST.get("reflag","")
        # 2. 查询数据库中账号密码
        try:
            user = UserInfo.objects.filter(uname=uname,pwd=pwd)[0] # user是列表
        except:
            return redirect("/userapp/register/")

        # 3. 如果有该用户，将用户存放在session中，跳转到个人中心页面，如果没有，跳到登录页面
        if user:
            request.session["user"] = jsonpickle.dumps(user)    # 用户对象序列化为字符串
            if reflag == "cartapp":
            # 将用户session中购物车数据存储到数据库
                SessionCartManager(request.session).migrateSession2DB()
                # 从购物车跳到登录，若登录成功，跳转到订单
                return redirect("/cartapp/queryAll/")
            elif reflag == "orderapp":
                # 获取表单中的数据
                cartitems = request.POST.get("cartitems")
                # 从结算页面跳转到登录页面,如果登录成功，跳转到确认订单
                totalPrice = request.POST.get("totalPrice")
                return redirect("/orderapp/toOrder/?cartitems="+cartitems+"&totalPrice="+totalPrice,)
            return redirect("/userapp/center/")
        return redirect("/userapp/login/")
def loadCode(request):
    """加载验证码"""
    img = ImageCaptcha()
    # 获取生成的验证码
    code = gene_text()
    # 将code存到session中
    request.session["session_code"] = code
    imgObj = img.generate(code)
    # 返回图片
    return HttpResponse(imgObj,content_type="img/png")

def checkcode(request):
    """校验输入的验证码是否正确"""
    # 获取输入的验证码
    code = request.GET.get("code",-1)
    # 获取session对象
    session_code = request.session.get("session_code",-2)
    # 判断是否相等
    vflag = False
    if code == session_code:
        vflag = True
    # 返回响应
    return JsonResponse({"vflag":vflag})

def loginout(request):
    """退出登录"""
    # 删除session对象及数据库中数据
    request.session.flush()
    # 返回响应
    return JsonResponse({"loginout":True})

class AddressView(View):
    """地址管理"""
    def post(self,request):
        # 获取表单数据
        aname = request.POST.get("aname","")
        aphone = request.POST.get("aphone","")
        addr = request.POST.get("addr","")
        # 从session中获取当前登录用户
        userinfo = request.session.get("user","")
        if userinfo:
            user = jsonpickle.loads(userinfo)


        # 设置是否是默认地址
        # 根据当前当前登录的用户，获取地址，查看是否是第一个地址
        count = user.address_set.count()
        if count == 0:
            isdefault = True
        else:
            isdefault = False
        # 插入数据库
        Address.objects.create(aname = aname,aphone=aphone,addr=addr,userinfo=user,isdefault=isdefault)
        return redirect("/userapp/address/")
    def get(self,request):
        # 获取当前登录用户
        userinfo = request.session.get("user","")
        if userinfo:
            user = jsonpickle.loads(userinfo)

        # 获取当前登录用户关联的收货地址
        addr_list = user.address_set.all()
        context = {
            "addr_list":addr_list,
        }
        return render(request,"userapp/address.html",context=context)

def loadArea(request):
    """级联加载地址"""
    pid = request.GET.get("pid",-1)
    # 根据pid查询数据
    areaList = Area.objects.filter(parentid=pid)
    # 返回响应
    return JsonResponse({"areaList":serializers.serialize("json",areaList)})

def updateDefaultAddrView(request):
    """设置默认地址"""
    # 获取请求参数addrId
    addrId = int(request.GET.get("addrId",-1))
    # 修改当前登录用户的默认地址
    # 从session中获取当前用户
    userinfo = request.session.get("user","")
    if userinfo:
        user = jsonpickle.loads(userinfo)
        # 获取当前用户所有地址
        addressList = user.address_set.all()
        # 
        for address in addressList:
            if address.id == addrId:
                address.isdefault = True
            else:
                address.isdefault = False
            address.save()
        return redirect("/userapp/address/")
