#!/bin/zsh
if ! [ -e bin/docs ]
then
    ./bin/buildout -c docs.cfg
fi
./bin/docs
