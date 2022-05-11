import jsonpickle
from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from alipay import AliPay

# Create your views here.
from django.views import View

from cart.cartmanager import getCartManger
from cart.models import CartItem
from goods.models import Inventory
from order.models import Order, OrderItem
from userapp.models import Address


class ToOrderView(View):
    def get(self, request):
        # 获取请求参数
        cartitems = request.GET.get('cartitems', '')

        # 判断用户是否登录
        if not request.session.get('user'):
            return render(request, 'login.html', {'cartitems': cartitems, 'redirect': 'order'})

        return HttpResponseRedirect('/order/order.html?cartitems=' + cartitems)


class OrderListView(View):
    def get(self, request):
        # 获取请求参数
        cartitems = request.GET.get('cartitems', '')

        # 将json格式字符串转换成python对象（字典{goodsid:1,colorid:1,sizeid:1}）列表
        # [ {goodsid:1,colorid:1,sizeid:1},{goodsid:1,colorid:1,sizeid:1}]
        # 根据上面的三要素来获取cartitem的对象，就是一件商品
        cartitemList = jsonpickle.loads("[" + cartitems + "]")
        #print(cartitemList)
        # 将python对象列表转换成CartItem对象列表
        cartitemObjList = [getCartManger(request).get_cartitems(**item) for item in cartitemList if item]

        # 获取用户的默认收货地址
        address = request.session.get('user').address_set.get(isdefault=True)

        # 获取支付总金额
        totalPrice=0
        for cm in cartitemObjList:
            totalPrice += cm.getTotalPrice()

        return render(request, 'order.html',
                      {'cartitemObjList': cartitemObjList, 'address': address, 'totalPrice': totalPrice})


''' 需要时去掉注释 并且填上支付宝公钥和应用私钥还要appid

# 支付宝公钥
alipay_public_key = """-----BEGIN PUBLIC KEY-----

-----END PUBLIC KEY-----"""

# 应用私钥
my_private_key = """-----BEGIN RSA PRIVATE KEY-----

-----END RSA PRIVATE KEY-----"""

# 创建AliPay对象
alipay = AliPay(
    appid='',
    app_notify_url='http://127.0.0.1:8000/order/checkPay/',
    app_private_key_string=my_private_key,
    alipay_public_key_string=alipay_public_key,
    sign_type='RSA2',
    debug=True
)


class ToPayView(View):
    def get(self, request):
        # 插入order表中数据
        # 获取请求参数
        import uuid, datetime
        data = {
            'out_trade_num': uuid.uuid4().hex,
            'order_num': datetime.datetime.today().strftime('%Y%m%d%H%M%S'),
            'payway': request.GET.get('payway'),
            'address': Address.objects.get(id=request.GET.get('address', '')),
            'user': request.session.get('user', '')
        }

        orderObj = Order.objects.create(**data)

        # 插入orderitem表中数据
        cartitems = jsonpickle.loads(request.GET.get('cartitems'))

        orderItemList = [OrderItem.objects.create(order=orderObj, **item) for item in cartitems if item]

        totalPrice = request.GET.get('totalPrice')[1:]

        # 获取扫码支付的页面
        params = alipay.api_alipay_trade_page_pay(
            subject='网上商城',
            out_trade_no=orderObj.out_trade_num,
            total_amount=str(totalPrice),
            return_url='http://127.0.0.1:8000/order/checkPay/'
        )

        # 拼接请求地址
        url = 'https://openapi.alipaydev.com/gateway.do' + '?' + params
        return HttpResponseRedirect(url)


class CheckPayView(View):
    def get(self, request):
        # 校验是否支付成功(验签过程)
        params = request.GET.dict()
        # 获取签名
        sign = params.pop('sign')
        if alipay.verify(params, sign):
            # 修改订单表中支付状态
            out_trade_no=params.get('out_trade_no','')
            order=Order.objects.get(out_trade_num=out_trade_no)
            order.status=u'待收货'
            order.save()

            # 修改库存 修改购物车
            orderitemList=order.orderitem_set.all()
            [Inventory.objects.filter(goods_id=item.goodsid,size_id=item.sizeid,color_id=item.colorid).update(count=F('count')-item.count) for item in orderitemList if item]
            [CartItem.objects.filter(goodsid=item.goodsid, sizeid=item.sizeid, colorid=item.colorid).delete() for item in orderitemList if item]


            # 这里没继续写了 有需求可以自己补充
            return HttpResponse('成功')
        return HttpResponse('失败')

'''