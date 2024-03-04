#!/bin/bash

init() {
    if ! which rye &> /dev/null
    then
        curl -sSf https://rye-up.com/get | bash
        echo "rye installed"
    else
        echo "rye already installed"
    fi
    git init
    # rye pin 3.11
    # rye sync
}


init