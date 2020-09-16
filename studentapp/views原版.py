from django.shortcuts import render

# Create your views here.
from utils.response import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from modelapp.models import *
from studentapp.models import *
from studentapp.serializers import *

# 四种不同视图的开发方式
from rest_framework import views,mixins,generics,viewsets


class StudentAPIView(APIView):
    def get(self,request,*args,**kwargs):
        user_id = kwargs.get('id')
        print('用户id：',user_id)
        if user_id:
            stu_obj=Student.objects.get(id=user_id)
            data =StudentSerializers(stu_obj).data
            # print(Student)
            # return Response({
            #     'status':200,
            #     "message": "查询单个用户成功",
            #     "results": Student
            # })
            return APIResponse(data=data,data_message='查询成功',data_status=200)
        else:
            stu_obj = Student.objects.all()
            data = StudentSerializers(stu_obj,many=True).data
            return Response({
                'status': 200,
                "message": "查询所有用户成功",
                "results": data
            })
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = StudentSerializers(data=data)
        # 校验数据是否合法 raise_exception=True  一旦校验失败 立即抛出异常
        serializer.is_valid(raise_exception=True)
        stu_obj = serializer.save()
        return Response({
            "status": 201,
            "message": "创建图书成功",
            "results": StudentSerializers(stu_obj).data
        })

# --------------------------------------------------------

class StudentAPIViewV2(APIView):
    """
    整合序列化器后的视图
    """

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:
            # 查询单个图书
            book_obj = Student.objects.get(id=book_id)
            data = StudentModelSerializer(book_obj).data
            return Response({
                "status": 200,
                "message": "查询单个图书成功",
                "results": data
            })
        else:
            objects_all = Student.objects.filter()
            user_list = StudentModelSerializer(objects_all, many=True).data
            return Response({
                "status": 200,
                "message": "查询所有成功",
                'results': user_list
            })
    def post(self, request, *args, **kwargs):
        """
        新增单个：传递参数的格式 字典
        新增多个：[{},{},{}]  列表中嵌套字典  每一个字典是一个图书对象
        """
        request_data = request.data
        # 代表添加单个对象
        if isinstance(request_data, dict):
            many = False
        # 代表添加多个对象
        elif isinstance(request_data, list):
            many = True
        else:
            return Response({
                "status": 400,
                "message": "数据格式有误"
            })

        book_obj = StudentModelSerializer(data=request_data, many=many)
        book_obj.is_valid(raise_exception=True)
        save = book_obj.save()

        return Response({
            "status": 200,
            "message": '添加图书成功',
            "results": StudentModelSerializer(save, many=many).data
        })

    def delete(self, request, *args, **kwargs):
        """
        单个删除：获取删除的id  根据id删除  通过动态路由传参 v2/books/1/  {ids:[1,]}
        删除多个：有多个id的时候 {ids:[1,2,3]}
        """
        book_id = kwargs.get("id")

        if book_id:
            # 删除单个  将删除单个转换为删除多个的参数形式
            ids = [book_id]
        else:
            # 删除多个
            ids = request.data.get("ids")

        # 判断传递过来的图书的id是否在数据库中  且还未删除
        response = Student.objects.filter(pk__in=ids).delete()
        print(response)
        if response:
            return Response({
                "status": 200,
                "message": "删除成功"
            })
        return Response({
            "status": 400,
            "message": "删除失败或者图书不存在",
        })

    def put(self, request, *args, **kwargs):
        """
        整体修改单个：修改一个对象的全部字段
        :return 修改后的对象
        """
        # 修改的参数
        request_data = request.data
        # 要修改的图书的id
        book_id = kwargs.get("id")
        # 如果id存在且传递的request_data是字典格式  代表单个修改  群改一个
        if book_id and isinstance(request_data, dict):
            book_ids = [book_id, ]  # [1]
            request_data = [request_data]  # [{}]
        # 如果id不存在  传递的参数是列表  修改多个
        elif not book_id and isinstance(request_data, list):
            book_ids = []

            # 将要修改的图书的id放入book_ids中
            for dic in request_data:
                pk = dic.pop("id", None)
                if pk:
                    book_ids.append(pk)
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": 'id不存在',
                    })
                # 参数格式有误
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": '参数有误',
            })
        # 前端发送的修改的值需要做安全校验
        # 更新参数的时候使用序列化器完成数据的校验
        # TODO 如果当前要局部修改则需指定 partial = True即可
        user_list = []  # 所有要修改的图书对象
        for pk in book_ids:
            try:
                book_obj = Student.objects.get(pk=pk)
                user_list.append(book_obj)
            except:
                # 如果图书对象不存在 将id与对应的数据移除
                index = book_ids.index(pk)
                request_data.pop(index)
                # print(request_data)

        book_ser = StudentModelSerializer(data=request_data,
                                         instance=user_list,
                                         context={"request": request},
                                         many=True)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()

        return Response({
            "status": status.HTTP_200_OK,
            "message": "批量更新成功",
        })
    def patch(self, request, *args, **kwargs):
        """
        局部更新
        """
        # 修改的参数
        request_data = request.data
        # 要修改的图书的id
        book_id = kwargs.get("id")
        # 如果id存在且传递的request_data是字典格式  代表单个修改  群改一个
        if book_id and isinstance(request_data, dict):
            book_ids = [book_id, ]  # [1]
            request_data = [request_data]  # [{}]
        # 如果id不存在  传递的参数是列表  修改多个
        elif not book_id and isinstance(request_data, list):
            book_ids = []

            # 将要修改的图书的id放入book_ids中
            for dic in request_data:
                pk = dic.pop("id", None)
                if pk:
                    book_ids.append(pk)
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": 'id不存在',
                    })
                # 参数格式有误
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": '参数有误',
            })
        # 前端发送的修改的值需要做安全校验
        # 更新参数的时候使用序列化器完成数据的校验
        # TODO 如果当前要局部修改则需指定 partial = True即可
        user_list = []  # 所有要修改的图书对象
        for pk in book_ids:
            try:
                book_obj = Student.objects.get(pk=pk)
                user_list.append(book_obj)
            except:
                # 如果图书对象不存在 将id与对应的数据移除
                index = book_ids.index(pk)
                request_data.pop(index)
                # print(request_data)

        book_ser = StudentModelSerializer(data=request_data,
                                         instance=user_list,
                                         partial=True,
                                         context={"request": request},
                                         many=True)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()

        return Response({
            "status": status.HTTP_200_OK,
            "message": "批量更新成功",
        })