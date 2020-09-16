'''

DRF中有四⼤视图组件： views、generics、mixins、viewsets
views ：DRF基本的视图模块，提供基本的视图访问⽅式
generics ：⼯具视图，提供了许多内置的⼯具，主要提供（
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"
）
同时也能提供一些自己的简化操作（
class BookGenericMixinView(ListAPIView, RetrieveAPIView, CreateAPIView):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"
）
mixins ：五⼤⼯具类并且是基于generics的三个设置，分别提供不同的操作（
                            ListModelMixin,
                         RetrieveModelMixin,
                         CreateModelMixin,
                         UpdateModelMixin,
                         DestroyModelMixin,
                         GenericAPIView）
viewsets ：视图集，主要用来自定义发送不了的类型，比如登录发post请求，但是不存数据，
所以不满足工具中的post请求，需要自己定义{
1. `ViewSet与GenericViewSet`都继承了ViewSetMixin，所两者的视图都可以在`as_view`⾃定义http
请求映射的函数视图
2. `GenericViewSet`继承视图是`GenericAPIView`，所以继承了`GenericViewSet`的视图可以与
mixins联合使⽤
3. `ViewSet`继承的事`APIView`，不能与mixins连⽤，所有逻辑需要⾃⼰实现
这种⽅式适合不要model参与的业务，或者是不是标准的http接⼝ 登录 注销
4. `ModelViewSet`继承了`GenericViewSet`与`mixins`的五个⼯具类，所以有六种常⻅的API操作
}
'''