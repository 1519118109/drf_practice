from rest_framework import serializers, exceptions

from drf_practice import settings
from serializersapp.models import Employee


class EmployeeSerializers(serializers.Serializer):
    # 变量必须是model中有的字段
    username=serializers.CharField()
    password = serializers.CharField()
    # 定义models中不存在的字段  SerializerMethodField()
    aaa = serializers.SerializerMethodField()
    def get_aaa(self, obj):
        return "aaa"
    # 对于参数值是可选的，可以利用get_变量名来设置对应值
    gender = serializers.SerializerMethodField()
    def get_gender(self,obj):
        # get_变量名_display()display能自动对应0：male,1:famale,2:others
        return obj.get_gender_display()

    pic = serializers.SerializerMethodField()
    def get_pic(self, obj):
        print(obj.pic)
        #注意，返回绝对路径才能访问图片 http://127.0.0.1:8000/media/pic/1111.jpg
        return "%s%s%s" % ("http://127.0.0.1:8000", settings.MEDIA_URL, obj.pic)


class EmployeeDeSerializers(serializers.Serializer):
    """
    反序列化：将前端提交的数据保存入库
    1. 前端需要提供哪些字段
    2. 对前端提供数据做安全校验
    3. 哪些字段需要一些额外的安全校验
    反序列化是不存在自定义字段的
    """
    # 字段中添加校验规则
    username = serializers.CharField(
        max_length=8,
        min_length=2,
        # 为规则自定义错误信息
        error_messages={
            "max_length": "用户名太长",
            "min_length": "用户名太短",
        }
    )
    password = serializers.CharField()
    phone = serializers.CharField(min_length=11,max_length=11, required=True,
                                  error_messages={
                                      'min_length':'电话应该为十一位',
                                      'max_length': '电话应该为十一位'
                                  }
                                  )

    # 自定义字段  重复密码验证，验证之后就删除，不能在create中进行保存，传过去会出错，只是用来验证
    # re_pwd = serializers.CharField()

    # # 全局钩子  可以通过attrs获取到所有的参数
    # def validate(self, attrs):
    #     pwd = attrs.get("password")
    #     re_pwd = attrs.pop("re_pwd")
    #     # print(self,attrs)
    #     # 自定义校验规则  两次密码不一致  则无法保存对象
    #     if pwd != re_pwd:
    #         raise exceptions.ValidationError("两次密码不一致")
    #     return attrs


    # 局部钩子： 可以对反序列化中的某个字段进行校验
    # validate_想验证的字段名
    def validate_username(self, value):
        # 对于可以为空的字段，可以验证不通过，比如validate_phone
        print("1111", value, type(value))
        if "王" in value:
            raise exceptions.ValidationError("用户名有误")

        return value
    def create(self, validated_data):
        """
        在保存用户对象时需要重写此方法完成保存
        validated_data: 前端传递的需要保存的数据
        """
        # print(validated_data)
        return Employee.objects.create(**validated_data)
