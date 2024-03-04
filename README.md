# coral node 模版
 
## 运行
```
pip install cookiecutter
cookiecutter https://github.com/EdgeGalaxy/CoralNodeTemplate.git
```


## 配置参数

### 配置文件
```json
{
  "username": "zhaokefei",
  "email": "zhaokefei5461@gmail.com",
  "node_name": "coral-node",
  "node_slug": "{{ cookiecutter.node_name | lower | replace('-', '_') }}",
  "node_desc": "coral node for {{ cookiecutter.node_slug }}",
  "node_cls": "{{ cookiecutter.node_name | replace('-', ' ') | replace('_', ' ') | capitalize | replace(' ', '')}}",
  "node_type": ["DataProducerNode", "RecognitionNode", "BusinessNode", "MediaProcessNode"],
  "receiver_node": ""
}
```

### 配置项
- node_name: 节点名称
- node_slug: 节点文件夹名，一般采用默认值
- node_desc: 节点描述
- node_cls: 节点类名
- node_type: 节点类型
  - DataProducerNode: 数据生产节点
  - RecognitionNode: yolo节点
  - BusinessNode: 业务节点
  - MediaProcessNode: 结束节点
- receiver_node: 接收节点, 非数据生产节点时必填


## 初始化项目操作

### 包管理工具

采用 [rye](https://rye-up.com/) 作为包管理工具

常规操作：
1. `rye add <package>` :指定包名，添加包到项目
2. `rye sync` : 更新项目依赖包
