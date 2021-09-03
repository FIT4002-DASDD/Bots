#!/bin/bash

# Update yum packages
sudo yum update -y

# Install node
if ! command -v node &>/dev/null; then
  echo "Node not found, installing..."
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
  . ~/.nvm/nvm.sh
  nvm install node
fi

# Install bazel via bazelisk
if ! command -v bazel &>/dev/null; then
  echo "Bazel not found, installing..."
  npm install -g @bazel/bazelisk
fi

# Install firefox (see: https://gist.github.com/lumodon/50d2a97b49056f52b1d5c7a63b9ed979_
if ! command -v firefox &>/dev/null; then
  wget "https://download.mozilla.org/?product=firefox-latest-ssl&os=linux&lang=en-US" -O "firefox.bz2"
  sudo tar -xvf $(echo firefox*)
  sudo ln -s /usr/local/firefox/firefox /usr/bin/firefox
  sudo yum install -y nss zlib sqlite java xvfb xorg-x11-server-Xvfb libvpx glibc.i686 libgcc_s.so.1 libstdc++.so.6 libatomic.so.1 libgtk-3.so.0 libdbus-glib-1.so.2 libXt.so.6
fi

# Install AWS SDK dependencies (TODO)
