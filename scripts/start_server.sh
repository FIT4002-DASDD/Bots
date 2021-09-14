#!/bin/bash

BASEDIR=$(dirname $0)

# Build bot binary
echo "-------Building bot with Bazel-------"
bazel build //bot:app

# Run bot scheduler
echo "-------Running bot scheduler-------"
python3 ${BASEDIR}/bot_scheduler.py