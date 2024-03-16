import time

from typing import Dict

from pydantic import Field
{%- if cookiecutter.node_type == 'input' %}
import numpy as np
from coral import CoralNode, BaseParamsModel, FirstPayload, RawPayload, RTManager, PTManager, NodeType
{%- elif cookiecutter.node_type == 'interface' %}
from coral import CoralNode, BaseParamsModel, PTManager, ObjectsPayload, InterfaceMode, NodeType
{%- elif cookiecutter.node_type == 'output' %}
from coral import CoralNode, BaseParamsModel, RawPayload, PTManager, NodeType
{%- else %}
from coral import CoralNode, BaseParamsModel, NodeType, ReturnPayloadWithTS, RawPayload,  RTManager, PTManager
{%- endif %}

from algrothms.core import {{ cookiecutter.node_cls }}Core


{%- if cookiecutter.node_type == 'trigger' %}
@RTManager.register()
class {{cookiecutter.node_cls}}ReturnPayload(ReturnPayloadWithTS):
    pass
{%- elif cookiecutter.node_type == 'rule' %}
@RTManager.register()
class {{cookiecutter.node_cls}}ReturnPayload(ReturnPayloadWithTS):
    pass
{%- endif %}


@PTManager.register()
class {{cookiecutter.node_cls}}ParamsModel(BaseParamsModel):
    # 可更改的参数，遵循pydantic的格式
    {%- if cookiecutter.node_type == 'interface' %}
    weight_fp: str = 'model.pt'
    {%- endif %}
    timestamp: float = Field(default_factory=lambda: time.time())


class {{cookiecutter.node_cls}}(CoralNode):

    # 配置文件，默认文件config.json, 可通过环境变量 CORAL_NODE_CONFIG_PATH 覆盖
    node_name = '{{ cookiecutter.node_name_cn }}'
    node_desc = '{{ cookiecutter.node_desc }}'
    config_path = 'config.json'
    node_type = NodeType.{{ cookiecutter.node_type }}

    def init(self, context: dict):
        """
        初始化参数，可传递到sender方法中

        :param context: 上下文参数
        """
        # 获取入参
        print(self.params.timestamp)
        {%- if cookiecutter.node_type == 'interface' %}
        model = {{ cookiecutter.node_cls }}Core(self.params.weight_fp)
        context['model'] = model
        {%- endif %}
        context['timestamp'] = time.time()


    {%- if cookiecutter.node_type == 'output' %}
    def sender(self, payload: RawPayload, context: Dict) -> None:
    {%- elif cookiecutter.node_type == 'interface' %}
    def sender(self, payload: RawPayload, context: Dict) -> ObjectsPayload:
    {%- elif cookiecutter.node_type == 'input' %}
    def sender(self, payload: RawPayload, context: Dict) -> FirstPayload:
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
        {%- if cookiecutter.node_type == 'input' %}
        raw = np.zeros((640, 640, 3), np.uint8)
        raw[:] = (255, 0, 0)
        return FirstPayload(raw=raw)
        {%- elif cookiecutter.node_type == 'interface' %}
        data = context['model'].predict(payload.raw)
        return ObjectsPayload(objects=data, mode=InterfaceMode.APPEND)
        {%- elif cookiecutter.node_type == 'output' %}
        return None
        {%- else %}
        return {{ cookiecutter.node_cls }}ReturnPayload()
        {%- endif %}



if __name__ == '__main__':
    # 脚本入口，包括注册和启动
    import os
    run_type = os.getenv("CORAL_NODE_RUN_TYPE", "run")
    if run_type == 'register':
        {{cookiecutter.node_cls}}.node_register()
    else:
        {{cookiecutter.node_cls}}().run()