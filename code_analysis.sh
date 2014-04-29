#!/bin/bash
# to get rid of the pylint warning "'No config file found, ...":
# try running pylint --generate-rcfile > .pylintrc
#

echo "PYLINT"
pylint --reports=n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" `find . -iname "*.py"`

echo ""
echo "PEP8"
pep8 `find . -iname "*.py"`

