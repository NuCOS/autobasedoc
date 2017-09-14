#!/bin/bash
PACKAGE=autobasedoc
VENV=./venv
if [ -d "$VENV" ]; then
  echo "remove virtual env first"
  sleep 2
  rm -rf "$VENV"
fi


###################################
echo "----------------------------------------------------"
{
conda create --name $PACKAGE'3_6' python=3.6 -y
source activate $PACKAGE'3_6'
} || { 
virtualenv -p $(which python3) $VENV/py3
source $VENV/py3/bin/activate 
}
pip install --upgrade pip
pip install nose2
pip install numpy
pip install matplotlib
python setup.py sdist

###################################
echo "----------------------------------------------------"
sleep 1
echo "python used: "
which python
python info.py
###################################
echo "----------------------------------------------------"
sleep 1
echo "now install the autobasedoc in python 3"
python setup.py install test
####################################
echo "----------------------------------------------------"
sleep 1
echo "now run test in py3"
nose2 --plugin nose2.plugins.junitxml --junit-xml
python aftermath.py nose2-junit.xml py3
echo "test done in:"
python info.py
sleep 3

source deactivate
echo "after deactivate"
python info.py

