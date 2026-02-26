#!/usr/bin/env bash

# Force Python version
export PYTHON_VERSION=3.11.7

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt