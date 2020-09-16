from rest_framework import serializers, exceptions

from drf_practice import settings
from studentapp.models import Student

class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    extra_kwargs = {
        'username': {
            "max_length": 20,  # 设置当前字段的最大长度
            "min_length": 1,
            "error_messages": {
                "max_length": "长度太长了",
                "min_length": "长度太短了",
            }
        }
    }

    # 全局钩子
    def validate(self, attrs):
        stu_number = attrs.get("stu_number")
        user = Student.objects.filter(stu_number=stu_number)
        if user:
            raise exceptions.ValidationError('学号已存在')
        return attrs

class StudentListSerializer(serializers.ListSerializer):
    # 重写update方法完成批量更新
    def update(self, instance, validated_data):
        for index, obj in enumerate(instance):
            # print(index)
            # print(obj)
            # print(validated_data[index])
            # TODO 每遍历一次 改变一下下标以及对应值和对象
            self.child.update(obj, validated_data[index])

        return instance

class StudentModelSerializer(serializers.ModelSerializer):
    """
    序列化器与反序列化器整合
    """
    class Meta:
        # 为修改多个图书提供ListSerializer
        list_serializer_class = StudentListSerializer

        model = Student

        # 指定的字段  填序列化与反序列所需字段并集
        fields = ("username", "stu_number", "img", "phone", "gender")

        # 添加DRF的校验规则  可以通过此参数指定哪些字段只参加序列化  哪些字段只参加反序列化
        extra_kwargs = {
            'book_name':{
            "max_length": 20,  # 设置当前字段的最大长度
            "min_length": 1,
                "error_messages": {
                    "max_length": "长度太长了",
                    "min_length": "长度太短了",
                }
            },
            # 只参与反序列化
            "stu_number": {
                "write_only": True,
            },
            # # 只参与序列化
            # "img": {
            #     "read_only": True
            # }
        }
        # 全局钩子

    def validate(self, attrs):
        stu_number = attrs.get("stu_number")
        user = Student.objects.filter(stu_number=stu_number)
        if user:
            raise exceptions.ValidationError('学号已存在')
        return attrs