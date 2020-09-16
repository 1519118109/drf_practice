from rest_framework import serializers, exceptions

from drf_practice import settings
from modelapp.models import *
from serializersapp.models import Employee

class PressModelSerializer(serializers.ModelSerializer):
    """
    出版社的序列化器
    """

    class Meta:
        model = Press
        fields = ("press_name", 'address', "img")

class BookSerializers(serializers.ModelSerializer):

    publish = PressModelSerializer()

    class Meta:
        # 指定当前序列化器要序列化哪个模型
        model = Book

        fields = ("book_name", "price", "img",'publish')

        # 指定你要序列化模型的哪些字段
        # fields = ("book_name", "price", "img",'press_address','author_list')
        # 可以直接查询表的所有字段
        # fields = "__all__"
        # 指定不展示哪些字段
        # exclude = ("is_delete", "status", "id")
        # 指定查询的深度
        # depth = 1

class BookDeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
    extra_kwargs={
        'book_name':{
            "max_length": 20,  # 设置当前字段的最大长度
            "min_length": 1,
                "error_messages": {
                    "max_length": "长度太长了",
                    "min_length": "长度太短了",
                }
        },
        "price": {
            "required": True,
            "decimal_places": 2,
        }
    }

    # 全局钩子
    def validate(self, attrs):
        name = attrs.get("book_name")
        book = Book.objects.filter(book_name=name)
        if book:
            raise exceptions.ValidationError('图书名已存在')
        return attrs

    # 局部钩子
    def validate_price(self, value):
        if value > 50000:
            raise exceptions.ValidationError("价格最多不能超过50000")
        return value


class BookListSerializer(serializers.ListSerializer):
    """
    使用此序列化器完成同时修改多个对象
    """

    # 重写update方法完成批量更新
    def update(self, instance, validated_data):
        # 要修改的对象  要修改的值
        # print(self)     # 当前调用的序列化器类
        # print(instance)  # 要修改的对象
        # print(validated_data)  # 要修改的值
        # print("1111", self.child)

        # 将群改修改成每次修改一个
        for index, obj in enumerate(instance):
            # print(index)
            # print(obj)
            # print(validated_data[index])
            # TODO 每遍历一次 改变一下下标以及对应值和对象
            self.child.update(obj, validated_data[index])

        return instance

class BookModelSerializer(serializers.ModelSerializer):
    """
    序列化器与反序列化器整合
    """
    class Meta:
        # 为修改多个图书提供ListSerializer
        list_serializer_class = BookListSerializer

        model = Book

        # 指定的字段  填序列化与反序列所需字段并集
        fields = ("book_name", "price", "img", "publish", "authors")

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
            "price": {
                "required": True,
                "decimal_places": 2,
            },
            # 只参与反序列化
            "publish": {
                "write_only": True,
            },
            "authors": {
                "write_only": True,
            },
            # 只参与序列化
            "pic": {
                "read_only": True
            }
        }

    # 全局钩子
    def validate(self, attrs):
        # 可以通过self.context获取到视图中传递过来的request对象
        # 比如前段传递密码过来，并不会发验证密码过来，但是会在request中呈现
        # 因为attrs展示出来的全部是参与序列化或者发反序列化的字段，而模型中没有此字段
        request = self.context.get("request")
        print('111',request.data)
        print('111',attrs)

        name = attrs.get("book_name")
        book = Book.objects.filter(book_name=name)
        if book:
            raise exceptions.ValidationError('图书名已存在')
        return attrs

    # 局部钩子
    def validate_price(self, value):
        if value > 50000:
            raise exceptions.ValidationError("价格最多不能超过50000")
        return value

    # # 重写update方法完成更新
    # def update(self, instance, validated_data):
    #     print(instance, "11111")
    #     print(validated_data)
    #     book_name = validated_data.get("book_name")
    #     instance.book_name = book_name
    #     instance.save()
    #     return instance