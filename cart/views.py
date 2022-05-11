from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .cartmanager import *
# Create your views here.
from django.views import View


class AddCartView(View):
    def post(self, request):
        # 在多级字典数据的时候需要手动设置modified = True ，实时的将数据存放到session中
        # 多级字典是指session是多级字典
        request.session.modified = True


        # print(request.POST)  # 这个request.post 接收回来的是个对象，这个对象底层是个字典类型，因为request本来就是携带回数据的
        # print(request.POST.dict())  # 加一个dict（），只是让他以字典形式出现而已
        # 1. 获取当前操作类型
        flag = request.POST.get('flag', '')

        # 2.判断当前的操作类型
        if flag == 'add':
            # 创建cartmanager对象
            carmanagerobj = getCartManger(request)
            # 加入购物车操作
            carmanagerobj.add(**request.POST.dict())
        elif flag == 'plus':
            carmanagerobj = getCartManger(request)
            #修改商品数量（添加）
            carmanagerobj.update(step=1,**request.POST.dict())
        elif flag == 'minus':
            carmanagerobj = getCartManger(request)
            # 修改商品数量（减少）
            carmanagerobj.update(step=-1, **request.POST.dict())
        elif flag == 'delete':
            carmanagerobj = getCartManger(request)
            # 修改商品数量（添加）
            carmanagerobj.delete(**request.POST.dict())

        return HttpResponseRedirect('/cart/queryAll/')


class CartListView(View):
    def get(self, request):
        # 创建cartmanager对象
        carmanagerobj = getCartManger(request)

        # 查询所有购物项信息
        cartlist = carmanagerobj.queryAll()

        return render(request, 'cart.html', {'cartlist': cartlist})
