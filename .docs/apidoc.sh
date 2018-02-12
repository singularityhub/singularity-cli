#!/bin/bash
# If the modules changed, the content of "source" should be backed up and
# new files generated (to update) by doing:
#
# sphinx-apidoc -o source/ ../spython

HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE=$(dirname $HERE)
cd $HERE
cd $BASE && python setup.py install && cd $HERE && make html
rm -rf $BASE/docs/api
mkdir -p $BASE/docs/api
mkdir -p $BASE/docs/api/assets
find $HERE/_build/html -exec sed -i -e 's/_static/assets/g' {} \;
cp -R $HERE/_build/html/_static/* $HERE/_build/html/assets
cp -R $HERE/_build/html/* $BASE/docs/api
