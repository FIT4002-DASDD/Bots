# FIT4002-DASDD-Bots

This is a project that consists of several subprojects that each make use of several technologies, including Python, Node.JS, Protocol Buffers, and C++. As such, the [Bazel](https://bazel.build/) build system is used.

## Prerequisites


Install Bazel:  https://docs.bazel.build/versions/main/install-ubuntu.html

## Build Twitter Bots


From the root of the project workspace, run: `bazel build //bot:app`

## Running the Twitter Bots

There are several required flags to run the python binary. Please pass in the:
```
--bot_username=<username of the bot to be run>
--bot_password=<password of the bot to be run>
--bot_output_directory=<full path to the directory where bot output will be stored>
```

Note: for the `--bot_output_directory` flag, please pass in the path to the `bot_out` folder included in this workspace.

### Bots run example

Call `bazel run`, passing in the flags discussed above (command for both bots are shown below). Change the bot_output_directory to the path on your machine:

`bazel run //bot:app -- --bot_username=Allison45555547 --bot_password=A2IHNDjPu23SNEjfy4ts --bot_output_directory=/home/akshay/Desktop/Uni/FIT4002/FIT4002-DASDD-Bots/bot_out`

`bazel run //bot:app -- --bot_username=ElizaHahns --bot_password=AKJHD97434%^% --bot_output_directory=/home/akshay/Desktop/Uni/FIT4002/FIT4002-DASDD-Bots/bot_out`



## Push Service Installation

TBD

## Push Service Usage
TBD
