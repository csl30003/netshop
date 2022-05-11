# coding=utf-8

def getUserInfo(request):
    return {'suser':request.session.get('user',None)}





