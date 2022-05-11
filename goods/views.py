from django.shortcuts import render

# Create your views here.
from django.views import View
from goods.models import *
from django.core.paginator import Paginator
import math


class IndexView(View):
    def get(self, request, cid=2, num=1, *args, **kwargs):
        cid = int(cid)
        num = int(num)

        # 查询所有类别信息
        categorys = Category.objects.all().order_by('id')

        # 查询当前类别下的所有商品信息
        goodsList = Goods.objects.filter(category_id=cid).order_by('id')

        # 分页 每页显示八条记录
        pager = Paginator(goodsList, 8)

        # 获取当前页的数据
        page_goodsList = pager.page(num)

        # 每页开始页码
        begin = (num - int(math.ceil(10.0 / 2)))
        if begin < 1:
            begin = 1

        # 每页结束页码
        end = begin + 9
        if end > pager.num_pages:
            end = pager.num_pages

        if end <= 10:
            begin = 1
        else:
            begin = end - 9

        pagelist = range(begin, end + 1)

        return render(request, 'index.html',
                      {'categorys': categorys, 'goodsList': page_goodsList, 'currentcid': cid, 'pagelist': pagelist,
                       'currentNum': num})


def recommed_view(func):  # 怎么说呢 因为现在只有女装的数据 其他的没有 如果你单纯浏览女装的东西 这方法相当于是历史记录了 但你浏览别的类别就不会推荐女装的东西了
    def wrapper(detailView, request, goodsid, *args, **kwargs):
        # 将存放在cookie中的goodsid获取
        cookie_str = request.COOKIES.get('recommend', '')

        # 存放goodsID放在里面
        goodsidlist = [gid for gid in cookie_str.split() if gid.strip()]

        # 最终需要获取的推荐商品
        goodsobjlist = [Goods.objects.get(id=gsid) for gsid in goodsidlist if
                        gsid != goodsid and Goods.objects.get(id=gsid).category_id == Goods.objects.get(id=goodsid).category_id][:4]
        # id对象放在里面就是id对应整个商品的属性 查询出来的是整个goodislist的所有对象，但是下面只显示四个，列表切片就可以了

        # 将 goodsliest 传给get方法
        response = func(detailView, request, goodsid, goodsobjlist, *args, **kwargs)
        # 这个地方你可以理解为调用了get方法，然后返回给了浏览器一个response对象了，只不过这个地方拿过来了，很基本的通用操作，注意一下

        # 判断 goodsid 是否存在goodsidlist中
        if goodsid in goodsidlist:
            goodsidlist.remove(goodsid)
            goodsidlist.insert(0, goodsid)
        else:
            goodsidlist.insert(0, goodsid)

        # 将goosidlist中的数据保存到cookid中
        response.set_cookie('recommend', ' '.join('%s' % gsid for gsid in goodsidlist), max_age=3 * 24 * 60 * 60)
        return response

    return wrapper


class DetailView(View):
    @recommed_view
    def get(self, request, goodsid, recommendlist=[]):
        goodsid = int(goodsid)

        # 根据goodsid查询商品详情信息，（goods对象）
        goods = Goods.objects.get(id=goodsid)

        category = Category.objects.get(id=goods.category_id).cname

        return render(request, 'detail.html', {'goods': goods, 'recommendlist': recommendlist, 'category': category})


class SearchView(View):
    def get(self, request, num=1, *args, **kwargs):
        num = int(num)

        search = request.GET.get('search', '')

        goods = Goods.objects.filter(gname__contains=search)

        return render(request, 'search.html', {'goods': goods})
