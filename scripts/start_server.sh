#!/bin/bash

BASEDIR=$(dirname $0)

# Build bot binary
echo "-------Building bot with Bazel-------"
bazel build //bot:app

# Build push service binary
echo "-------Building push service with Bazel-------"
bazel build //push-service:main --sandbox_writable_path=/home/ec2-user/.cache/bazel/

bazel shutdown  # stop bazel server to reduce memory consumption

# Run bot scheduler
echo "-------Running bot scheduler-------"
python3 ${BASEDIR}/bot_scheduler.py