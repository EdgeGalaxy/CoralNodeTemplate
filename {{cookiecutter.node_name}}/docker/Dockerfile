FROM python:3.11.7

WORKDIR /app

# install rye
RUN curl -sSf https://rye-up.com/get | bash

COPY pyproject.tom requirements.lock /app

# install package
RUN rye sync

COPY . /app

CMD source /app/.venv/bin/activate && cd /app/{{cookiecutter.node_name}} && python3 node.py