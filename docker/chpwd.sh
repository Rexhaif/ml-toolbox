#!/bin/bash

export HASHED_PASSWORD=$(python hashpwd.py $1)
print($HASHED_PASSWORD)
sed -i "s/# c.NotebookApp.password = u''/c.NotebookApp.password = u'$HASHED_PASSWORD'/g" /jupyter/jupyter_notebook_config.py
