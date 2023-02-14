import jsonpickle

def getUserInfo(request):
    """获取用户对象信息"""
    # 从session对象获取用户
    user = request.session.get("user")

    # 将字符串反序列化为对象
    if user:
        user = jsonpickle.loads(user)
    return {"userInfo":user}