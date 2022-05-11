from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from cart.cartmanager import SessionCartManager
from utils.code import *  # code是验证码的工具包

# Create your views here.
from django.views import View
from userapp.models import *
from django.core.serializers import serialize
from order.models import *


# Create your views here.
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 获取请求参数
        uname = request.POST.get('uname', '')
        pwd = request.POST.get('pwd', '')

        # 插入数据库
        user = UserInfo.objects.create(uname=uname, pwd=pwd)

        # 判断是否注册成功
        if user:
            # 将用户信息存放至session对象中
            request.session['user'] = user
            return HttpResponseRedirect('/user/center/')

        return HttpResponse('/user/register/')


class CheckUnameView(View):
    def get(self, request):
        # 获取请求参数
        uname = request.GET.get('uname', '')

        # 根据用户名去数据库中查询
        userlist = UserInfo.objects.filter(uname=uname)

        flag = False
        # 判断是否存在
        if userlist:
            flag = True

        return JsonResponse({'flag': flag})


class CenterView(View):
    def get(self, request):
        user = request.session.get('user', '')
        userid = UserInfo.objects.filter(uname=user.uname)[0].id

        orderlist = Order.objects.filter(user_id=userid)

        To_be_paid = 0
        Goods_to_be_received = 0
        for i in range(len(orderlist)):
            if orderlist[i].status == '待支付':
                To_be_paid += 1
            elif orderlist[i].status == '待收货':
                Goods_to_be_received += 1

        return render(request, 'center.html', {"To_be_paid": To_be_paid, "Goods_to_be_received": Goods_to_be_received})


class LogoutView(View):
    def post(self, request):
        # 删除session中登录用户信息
        if 'user' in request.session:
            del request.session['user']

        return JsonResponse({'delflag': True})


class LoginView(View):
    def get(self, request):
        # 获取请求参数
        red = request.GET.get('redirect', '')
        return render(request, 'login.html', {'redirect': red})

    def post(self, request):
        # 1.获取请求参数
        uname = request.POST.get('uname', '')
        pwd = request.POST.get('pwd', '')

        # 2.查询数据库中是否存在
        userlist = UserInfo.objects.filter(uname=uname, pwd=pwd)  # 这个是列表形式,是对象形式，就是什么信息都有

        if userlist:  # 这个地方为真不就是登录成功了吗
            request.session['user'] = userlist[0]

            red = request.POST.get('redirect', '')
            if red == 'cart':
                # 将session中的购物项移动到数据库，注意post请求是代表登录成功了，
                # 然后的话根据在session中保存的用户信息去增加数据
                SessionCartManager(request.session).migrateSession2DB()
                return HttpResponseRedirect('/cart/queryAll/')
            elif red == 'order':
                return HttpResponseRedirect('/order/order.html?cartitems=' + request.POST.get('cartitems', ''))

            return HttpResponseRedirect('/user/center/')
        return HttpResponseRedirect('/user/login/')


class LoadCodeView(View):
    def get(self, request):
        img, str = gene_code()

        # 将生成的验证码存放到session中
        request.session['sessionCode'] = str
        return HttpResponse(img, content_type='image/png')


class CheckCodeView(View):
    def get(self, request):
        # 获取输入框中的验证码
        code = request.GET.get('code', '')

        # 获取生成的验证码
        sessionCode = request.session.get('sessionCode', None)

        # 比较是否相等
        flag = code == sessionCode

        return JsonResponse({'checkFlag': flag})


class AddressView(View):
    def get(self, request):
        user = request.session.get('user', '')
        # 获取当前登录用户的所有地址
        addrlist = user.address_set.all()

        return render(request, 'address.html', {'addlist': addrlist})

    def post(self, request):
        # 获取请求参数
        aname = request.POST.get('aname', '')
        aphone = request.POST.get('aphone', '')
        addr = request.POST.get('addr', '')
        user = request.session.get('user', '')
        # 将数据插入数据库
        address = Address.objects.create(aname=aname, aphone=aphone, addr=addr, userinfo=user,
                                         isdefault=(lambda count: True if count == 0 else False)(
                                             user.address_set.all().count()))

        # 获取当前登录用户的所有地址
        addrlist = user.address_set.all()

        return render(request, 'address.html', {'addlist': addrlist})


class LoadAreaView(View):
    def get(self, request):
        # 获取请求参数
        pid = request.GET.get('pid', -1)
        pid = int(pid)

        # 根据父id查询区域信息
        arealist = Area.objects.filter(parentid=pid)
        # 进行序列化，把arealist 转成字符串格式了。
        jarealist = serialize('json', arealist)

        return JsonResponse({'jarealist': jarealist})
