#!/bin/zsh
if [ -e bin/docs ]
then
    ./bin/buildout
fi
./bin/nosetests -sv docs/update_tutorial_requests.py
