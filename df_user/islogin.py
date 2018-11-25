from django.http import HttpResponseRedirect

#如果登录则转到登录页面
def islogin(func):
    def login_fun(request,*args,**kwargs):
        if request.session.get('user_id'):
            return func(request,*args,**kwargs)
        else:
            red = HttpResponseRedirect('/user/login')
            '''
            http://127.0.0.1:8000/200/?type=10
            peruest.path：表示当前路径，为/200/
            request.get_full_path()：表示完整路径，为/200/?type=10
            '''
            # 记录登录页面
            red.set_cookie('url',request.get_full_path())
            return red
    return login_fun