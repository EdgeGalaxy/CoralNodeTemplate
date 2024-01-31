FROM python:3.11.7

# opencv 相关安装so文件
RUN apt-get update && apt-get install -y libgl1

WORKDIR /workspace

COPY ./requirements.lock /workspace
RUN sed '/-e/d' requirements.lock > requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD cd {{cookiecutter.node_name}} && python3 node.py