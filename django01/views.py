from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render,HttpResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt, csrf_protect


# @csrf_protect#为某个视图开启CSRF验证
from django01.models import User


@csrf_exempt#为某个视图解除CSRF验证
def user(request):
    if request.method=='GET':
        print('GET=>访问成功')
        print(request.GET.get('id'))
        return HttpResponse('GET=>访问成功')
    if request.method=='POST':
        print('POST=>访问成功')
        print(request.POST.get('id'))
        return HttpResponse('POST=>访问成功')
    if request.method=='PUT':
        print('PUT=>访问成功')
        # print(request.PUT.get('id'))
        return HttpResponse('PUT=>访问成功')
    if request.method=='DELETE':
        print('DELETE=>访问成功')
        # print(request.DELETE.get('id'))
        return HttpResponse('DELETE=>访问成功')

@method_decorator(csrf_exempt,name='dispatch')  #让类视图免除CSRF验证
class Userview(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        if user_id:  # 查询单个
            # user_obj = User.objects.get(pk=user_id)
            user_obj = User.objects.filter(id=user_id).values("username", "password", "gender", "email").first()
            print(user_obj, type(user_obj))
            if user_obj:
                # 如果查询出对应的用户信息，则将用户的信息返回到前台
                return JsonResponse({
                    "status": 200,
                    "message": "查询单个用户成功",
                    "results": user_obj
                })
        else:
            # 如果用户id为空，则代表要查询所有用户的信息
            user_list = User.objects.all().values("username", "password", "gender", "email")
            return JsonResponse({
                "status": 200,
                "message": "查询所有用户成功",
                "results": list(user_list)
            })

        return JsonResponse({
            "status": 500,
            "message": "查询用户不存在",
        })

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        try:
            user_obj = User.objects.create(username=username, password=password, email=email)
            return JsonResponse({
                "status": 200,
                "message": "创建用户成功",
                "results": {"username": user_obj.username, "email": user_obj.email}
            })
        except:
            return JsonResponse({
                "status": 500,
                "message": "创建用户失败",
            })
    def put(self,request,*args,**kwargs):
        print('PUT请求 查询')
        return HttpResponse('PUT 访问成功')
    def delete(self,request,*args,**kwargs):
        print('DELETE请求 查询')
        return HttpResponse('DELETE 访问成功')