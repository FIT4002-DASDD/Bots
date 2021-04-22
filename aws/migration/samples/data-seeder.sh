#!/bin/bash

MAX_COUNT=10
count=0

while [ $count -lt $MAX_COUNT ]; do
  num=$RANDOM
  echo "Configuring bot data for bot id: ${num}"
  wget -q https://picsum.photos/100/100.jpg -O images/${num}.jpg
  count=$((count + 1))
done
