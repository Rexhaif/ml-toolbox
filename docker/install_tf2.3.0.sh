#!/bin/bash
set -eo pipefail

echo "======================================================================================================================"
echo "======================================================================================================================"
echo "== Uninstalling existing tensorflow =="
echo "======================================================================================================================"
echo "======================================================================================================================"
pip uninstall -y tensorflow tensorflow-estimator tf-nightly || true

echo "======================================================================================================================"
echo "======================================================================================================================"
echo "== Installing tensorflow =="
echo "======================================================================================================================"
echo "======================================================================================================================"
pip install -U tensorflow==2.3.0

echo "======================================================================================================================"
echo "======================================================================================================================"
echo "== Testing gpu availability                                      =="
echo "== This should print list of gpu devices available in the system =="
echo "======================================================================================================================"
echo "======================================================================================================================"
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

