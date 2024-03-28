#!/bin/bash

init() {
    git init
	pip install -U pip -i https://mirrors.tencent.com/pypi/simple
	pip install pre-commit poetry==1.8.2 -i https://mirrors.tencent.com/pypi/simple
	pre-commit install
	pre-commit install --hook-type commit-msg
}

init_package() {
    poetry install
	poetry shell
}

init
init_package