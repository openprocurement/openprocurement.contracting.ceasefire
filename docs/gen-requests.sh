# check if there is buildout present
if [ ! -e bin/buildout ] || [ ! -e bin/nosetests ]
# if it isn't - create it
then
    python bootstrap.py
    ./bin/buildout
fi
# run the requests files generation
./bin/nosetests -sv docs/update_tutorial_requests.py
