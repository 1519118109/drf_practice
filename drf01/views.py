from django.shortcuts import render

# Create your views here.
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from rest_framework.views import APIView
from rest_framework.response import Response

from django01.models import User


class UserAPIView(APIView):
    # renderer_classes = (JSONRenderer,BrowsableAPIRenderer)
    # parser_classes = [JSONParser,]
    def get(self, request, *args, **kwargs):
        print("这是drf的get请求")
        #用于url路径中拼接参数的接收
        user_id = kwargs.get("id")
        #用于传参数的时候问号拼接的参数
        # user_id=request.query_params.get('id')
        # user_id = request.data.get('id')
        # user_id = request._request.GET.get('id')
        # user_id = request.GET.get('id')
        if user_id:  # 查询单个
            # user_obj = User.objects.get(pk=user_id)
            # 利用User.objects.get(pk=user_id)请求可以跳转到自定义的异常，filter此处不可以
            user_obj = User.objects.filter(id=int(user_id)).values("username", "password", "gender", "email").first()
            print(user_obj, type(user_obj))
            if user_obj:
                # 如果查询出对应的用户信息，则将用户的信息返回到前台
                return Response({
                    "status": 200,
                    "message": "查询单个用户成功",
                    "results": user_obj
                })
        # else:
        #     # 如果用户id为空，则代表要查询所有用户的信息
        #     user_list = User.objects.all().values("username", "password", "gender", "email")
        #     return Response({
        #         "status": 200,
        #         "message": "查询所有用户成功",
        #         "results": list(user_list)
        #     })
        #
        # return Response({
        #     "status": 500,
        #     "message": "查询用户不存在",
        # })
        # return Response


    def post(self, request, *args, **kwargs):
        # username = request.POST.get("username")
        # password = request.POST.get("password")
        # email = request.POST.get("email")

        # username = request._request.POST.get("username")
        # password = request._request.POST.get("password")
        # email = request._request.POST.get("email")

        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        print(username,password,email)
        try:
            user_obj = User.objects.create(username=username, password=password, email=email)
            return Response({
                "status": 200,
                "message": "创建用户成功",
                "results": {"username": user_obj.username, "email": user_obj.email}
            })
        except:
            return Response({
                "status": 500,
                "message": "创建用户失败",
            })

from rest_framework.views import exception_handler

class StudentAPIView(APIView):

    def get(self, request, *args, **kwargs):
        stu_id = kwargs.get("id")

        if stu_id:
            stu_obj = User.objects.get(pk=stu_id)
            return Response({
                "status": 200,
                "message": '查询单个用户成功',
                "results": {"username": stu_obj.username, "email": stu_obj.email}
            })