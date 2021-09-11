#!/bin/bash

BASEDIR=$(dirname $0)

# Install dependencies
echo "-------Installing dependencies-------"
${BASEDIR}/install_dependencies.sh

# Build bot binary
echo "-------Building bot with Bazel-------"
bazel build //bot:app

# Run bot scheduler
echo "-------Running bot scheduler-------"
# python3 ${BASEDIR}/bot_scheduler.py > /dev/null 2>&1
python3 ${BASEDIR}/bot_scheduler.py