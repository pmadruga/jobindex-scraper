#!/usr/bin/env bash
set -e

export FLASK_APP=app.py
export FLASK_DEBUG=1
export APP_CONFIG_FILE=config.py

flask run --host=0.0.0.0 --port=9003
