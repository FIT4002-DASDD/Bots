#!/bin/bash

# Update apt-get packages
sudo apt-get update -y

# Install python 3
if ! command -v python3 &>/dev/null; then
  sudo apt-get install python3 -y
fi

# Install node
if ! command -v npm &>/dev/null; then
  sudo apt-get install -y npm
fi

# Install bazel via bazelisk
if ! command -v bazel &>/dev/null; then
  echo "Bazel not found, installing..."
  sudo npm install -g @bazel/bazelisk
  sudo apt-get install gcc g++ -y
fi

# Install firefox (see: https://gist.github.com/lumodon/50d2a97b49056f52b1d5c7a63b9ed979_
if ! command -v firefox &>/dev/null; then
  sudo apt-get install -y firefox
fi

# Install AWS SDK dependencies
sudo apt-get -y install libcurl4-openssl-dev libssl-dev uuid-dev zlib1g-dev libpulse-dev

# Install Postgres connection service
sudo apt-get install -y libpq-dev

# Install cmake
if ! command -v cmake3 &>/dev/null; then
  sudo apt-get install -y cmake
fi
