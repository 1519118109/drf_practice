from rest_framework.response import Response

"""
data=None  响应的数据
status=None 响应的状态码
template_name=None 渲染的模板地址
headers=None	响应头
exception=False	是否有异常
content_type=None	数据格式  一般不处理
"""


class APIResponse(Response):

    def __init__(self, data_status=200, data_message=0, results=None,
                 http_status=None, headers=None, exception=False, **kwargs):
        # 定义响应回去的数据
        data = {
            "status": data_status,
            "message": data_message,
        }

        # 判断results是否有结果
        if results is not None:
            data['results'] = results

        # 如果还需要传递自定义的参数  使用kwargs接收
        # 如果kwargs有值则将值添加到 data中  如果没值则不作任何操作
        data.update(kwargs)

        # 获取一个response对象  将自定义的response响应回去
        super().__init__(data=data, status=http_status, headers=headers, exception=exception)
