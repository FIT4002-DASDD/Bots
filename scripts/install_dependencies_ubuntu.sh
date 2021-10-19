#!/bin/bash

# Update yum packages
sudo yum update -y

# Install python 3
if ! command -v python3 &>/dev/null; then
  sudo apt-get install python3 -y
fi

# Install node
if ! command -v nvm &>/dev/null; then
  echo "Node not found, installing..."
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
  . ~/.nvm/nvm.sh
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
  [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" 
fi
if ! command -v node &>/dev/null; then
  nvm install node
fi

# Install bazel via bazelisk
if ! command -v bazel &>/dev/null; then
  echo "Bazel not found, installing..."
  npm install -g @bazel/bazelisk
  sudo apt-get install gcc gcc-c++ -y
fi

# Install firefox (see: https://gist.github.com/lumodon/50d2a97b49056f52b1d5c7a63b9ed979_
if ! command -v firefox &>/dev/null; then
  wget "https://download.mozilla.org/?product=firefox-latest-ssl&os=linux&lang=en-US" -O "/usr/local/firefox.bz2"
  sudo tar -xvf $(echo /usr/local/firefox.bz2) -C /usr/local/
  sudo apt-get install -y nss zlib sqlite java xvfb xorg-x11-server-Xvfb libvpx glibc.i686 libgcc_s.so.1 libstdc++.so.6 libatomic.so.1 libgtk-3.so.0 libdbus-glib-1.so.2 libXt.so.6
fi

# Install AWS SDK dependencies
sudo apt-get -y install libcurl4-openssl-dev libssl-dev uuid-dev zlib1g-dev libpulse-dev

# Install Postgres connection service
sudo apt-get install -y libpq-dev

# Install cmake
if ! command -v cmake3 &>/dev/null; then
  sudo apt-get install -y cmake
fi

