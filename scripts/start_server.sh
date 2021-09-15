#!/bin/bash

BASEDIR=$(dirname $0)

# Build bot binary
echo "-------Building bot with Bazel-------"
bazel build //bot:app
bazel shutdown  # stop bazel server to reduce memory consumption

# Run bot scheduler
echo "-------Running bot scheduler-------"
python3 ${BASEDIR}/bot_scheduler.py