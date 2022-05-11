from django.db import models


# Create your models here.

class Category(models.Model):
    cname = models.CharField(max_length=10, verbose_name=u'类名')

    def __str__(self):
        return u'Category:%s' % self.cname


class Goods(models.Model):
    gname = models.CharField(max_length=100, verbose_name=u'商品名')
    gdesc = models.CharField(max_length=100, verbose_name=u'商品描述')
    oldprice = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=u'原价')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=u'现价')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=u'类别名称')

    # 这个地方是自己写类名对应的主键的ID，所以Category字段多少不影响

    def __str__(self):
        return u'Goods:%s' % self.gname

    # 获取商品大图
    def getGImg(self):
        return self.inventory_set.first().color.colorurl

    # 获取商品所有颜色对象 ，就是当点尺寸的时候这个颜色是不变的，所以说，获取了所有颜色，去重。放在列表里面，
    # 无论什么尺寸都是这几个固定的颜色
    def getColors(self):
        colorlist = []
        for inventory in self.inventory_set.all():
            color = inventory.color
            if color not in colorlist:
                colorlist.append(color)
        return colorlist

    def getSizelist(self):
        sizelist = []
        for inventory in self.inventory_set.all():
            size = inventory.size
            if size not in sizelist:
                sizelist.append(size)
        return sizelist

    # 获取所有详情信息
    def getDetaillist(self):
        import collections
        # 创建有序字典存放详情信息 key是详情名称，value是图片列表
        datas = collections.OrderedDict()
        for goodsdetail in self.goodsdetail_set.all():
            # 获取详情名称
            gdname = goodsdetail.name()

            if gdname not in datas.keys():  # 还有一种写法就是if not datas.get(gdname)
                datas[gdname] = [goodsdetail.gdurl]
            else:
                datas[gdname].append(goodsdetail.gdurl)

        return datas


class GoodsDetailName(models.Model):
    gdname = models.CharField(max_length=30, verbose_name=u'商品详情名称')

    def __str__(self):
        return u'GoodsDetailName:%s' % self.gdname


class GoodsDetail(models.Model):
    gdurl = models.ImageField(upload_to='', verbose_name=u'商品图片')
    gdname = models.ForeignKey(GoodsDetailName, on_delete=models.CASCADE, verbose_name=u'商品详情名称')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name=u'商品名')

    # 获取他的详情名称
    def name(self):
        return self.gdname.gdname


class Size(models.Model):
    sname = models.CharField(max_length=10, verbose_name=u'尺寸名')

    def __str__(self):
        return u'Size:%s' % self.sname


class Color(models.Model):
    colorname = models.CharField(max_length=10, verbose_name=u'颜色名')
    colorurl = models.ImageField(upload_to='color/', verbose_name=u'颜色图片')

    def __str__(self):
        return u'Color:%s' % self.colorname


class Inventory(models.Model):
    count = models.PositiveIntegerField(verbose_name=u'库存数量')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name=u'颜色名称')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name=u'商品名称')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name=u'尺寸名称')
