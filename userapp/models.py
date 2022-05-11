# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Area(models.Model):  # 这个地方是在写地址的时候有一个下拉菜单里面的东西
    areaid = models.IntegerField(primary_key=True)
    areaname = models.CharField(max_length=50)
    parentid = models.IntegerField()
    arealevel = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False  # 假如你要是在正向生成数据库表，这个就不会生成了，生成其他的。
        db_table = 'area'


class UserInfo(models.Model):
    uname = models.EmailField(max_length=100)  # 账户名，邮箱格式
    pwd = models.CharField(max_length=100)  # 登录密码
    head_portrait = models.ImageField(default="jd.webp")

    def __str__(self):
        return u'UserInfo:%s' % self.uname


class Address(models.Model):
    aname = models.CharField(max_length=30)  # 收件人姓名
    aphone = models.CharField(max_length=11)  # 收件人电话
    addr = models.CharField(max_length=100)  # 收件人地址
    isdefault = models.BooleanField(default=False)  # 是否是默认收货地址
    userinfo = models.ForeignKey(UserInfo, on_delete=models.CASCADE)  # 收件人的账户信息

    def __str__(self):
        return u'Address:%s' % self.aname