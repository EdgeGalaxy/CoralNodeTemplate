import time

from typing import Dict
{%- if cookiecutter.node_type == 'DataProducerNode' %}
from typing import Union, List

import numpy as np
from pydantic import Field
from coral import CoralNode, ParamsModel, FirstPayload, RawPayload, RTManager, PTManager
{%- elif cookiecutter.node_type == 'RecognitionNode' %}
from coral import CoralNode, ParamsModel, ObjectsPayload, RawPayload,  RTManager, PTManager
{%- elif cookiecutter.node_type == 'BusinessNode' %}
from coral import CoralNode, ParamsModel, ReturnPayload, RawPayload,  RTManager, PTManager
{%- elif cookiecutter.node_type == 'MediaProcessNode' %}
from coral import CoralNode, ParamsModel, RawPayload,  RTManager, PTManager
{%- endif %}

from algrothms.core import {{ cookiecutter.node_cls }}Algro


{%- if cookiecutter.node_type == 'DataProducerNode' %}
@RTManager.register()
class {{cookiecutter.node_cls}}ReturnPayload(FirstPayload):
    raw: List
{%- elif cookiecutter.node_type == 'BusinessNode' %}
@RTManager.register()
class {{cookiecutter.node_cls}}ReturnPayload(ReturnPayload):
    pass
{%- endif %}


@PTManager.register()
class {{cookiecutter.node_cls}}ParamsModel(ParamsModel):
    # 可更改的参数，遵循pydantic的格式
    {%- if cookiecutter.node_type == 'RecognitionNode' %}
    model_fp: str = 'model.pt'
    {%- endif %}
    timestamp: float = Field(default_factory=time.perf_counter)


class {{cookiecutter.node_cls}}(CoralNode):

    # 配置文件，默认文件config.json, 可通过环境变量 CORAL_NODE_CONFIG_PATH 覆盖
    node_name = '{{ cookiecutter.node_name_cn }}'
    node_desc = '{{ cookiecutter.node_desc }}'
    config_path = 'config.json'
    node_type = '{{ cookiecutter.node_type }}'

    def init(self, context: dict):
        """
        初始化参数，可传递到sender方法中

        :param context: 上下文参数
        """
        # 获取入参
        print(self.params.timestamp)
        {%- if cookiecutter.node_type == 'RecognitionNode' %}
        model = {{ cookiecutter.node_cls }}Algro(self.params.model_fp)
        context['model'] = model
        {%- endif %}
        context['timestamp'] = time.time()


    {%- if cookiecutter.node_type == 'MediaProcessNode' %}
    def sender(self, payload: RawPayload, context: Dict) -> None:
    {%- elif cookiecutter.node_type == 'RecognitionNode' %}
    def sender(self, payload: RawPayload, context: Dict) -> ObjectsPayload:
    {%- else %}
    def sender(self, payload: RawPayload, context: Dict) -> {{cookiecutter.node_cls}}ReturnPayload:
    {%- endif %}
        """
        数据发送函数

        :param payload: receiver的数据
        :param context: 上下文参数
        :return: 数据
        """
        print(context['timestamp'])
        {%- if cookiecutter.node_type == 'DataProducerNode' %}
        raw = np.zeros((640, 640, 3), np.uint8)
        raw[:] = (255, 0, 0)
        return {{cookiecutter.node_cls}}ReturnPayload(raw=raw)
        {%- elif cookiecutter.node_type == 'RecognitionNode' %}
        data = context['model'].predict(payload.raw)
        return ObjectsPayload(**data)
        {%- elif cookiecutter.node_type == 'BusinessNode' %}
        return {{ cookiecutter.node_cls }}ReturnPayload()
        {%- elif cookiecutter.node_type == 'MediaProcessNode' %}
        return None
        {%- endif %}



if __name__ == '__main__':
    # 脚本入口，包括注册和启动
    import os
    run_type = os.getenv("CORAL_NODE_RUN_TYPE", "run")
    if run_type == 'register':
        {{cookiecutter.node_cls}}.node_register()
    else:
        {{cookiecutter.node_cls}}().run()