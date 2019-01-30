# bootstrap the buildout if needed
if [ ! -e bin/buildout ]; then
    python bootstrap.py
fi

if [ ! -e bin/docs ]; then
    ./bin/buildout -c docs.cfg
fi

./bin/docs
