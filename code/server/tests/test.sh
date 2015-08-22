#!/bin/bash

export PYTHONPATH=code/server
export STORE_MONGO_PORT=5000

py.test --cov-config code/server/tests/.coveragerc --cov=code/server code/server/tests