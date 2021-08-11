#! /usr/bin/env bash

TARGET=//bot:app
BOT_OUT=/home/akshay/Desktop/Uni/FIT4002/FIT4002-DASDD-Bots/bot_out

usernames=("Allison45555547" "ElizaHahns")
passwords=("A2IHNDjPu23SNEjfy4ts" "AKJHD97434%^%")

for i in "${!usernames[@]}"; do
  echo bazel run ${TARGET} -- --bot_username="${usernames["${i}"]}" --bot_password="${passwords["${i}"]}" --bot_output_directory=${BOT_OUT} &
  bazel run ${TARGET} -- --bot_username="${usernames["${i}"]}" --bot_password="${passwords["${i}"]}" --bot_output_directory=${BOT_OUT} &
done
