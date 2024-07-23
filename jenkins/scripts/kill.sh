#!/usr/bin/env sh

set -x
docker kill my-python-app
docker rm my-python-app
