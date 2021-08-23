# FIT4002-DASDD-Bots

This is a project that consists of several subprojects that each make use of several technologies, including Python,
Node.JS, Protocol Buffers, and C++. As such, the [Bazel](https://bazel.build/) build system is used.

## Prerequisites

Install Bazel: https://docs.bazel.build/versions/main/install-ubuntu.html

## Running the E2E workflow

From the root of the project workspace, run the shell binary:
`./workflow_start.sh`

This will spin up the bot workflow for all configured bots in the shell script in the **background**.

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

Call `bazel run`, passing in the flags discussed above:

`bazel run //bot:app -- --bot_username=Allison45555547 --bot_password=A2IHNDjPu23SNEjfy4ts --bot_output_directory=/home/akshay/Desktop/Uni/FIT4002/FIT4002-DASDD-Bots/bot_out`

## Build Push Service

First install the AWS C++ SDK's dependencies by following
the [official docs](https://docs.aws.amazon.com/sdk-for-cpp/v1/developer-guide/setup-linux.html):

`sudo apt-get install libcurl4-openssl-dev libssl-dev uuid-dev zlib1g-dev libpulse-dev`

Call `bazel build` on the `//push-service:main` target, specifying the full path to the Bazel cache directory in
the `--sandbox_writable_path` flag:

Example: `bazel build //push-service:main --sandbox_writable_path=/home/runner/.cache/bazel/`

| :exclamation: **
NOTE:** You must specify the `--sandbox_writable_path` when building. It is necessary as the AWS SDK's CMake rules make
changes to the Bazel sandbox (which Bazel does not really like) - so this way we tell Bazel to expect that this
directory will be changed. | |-----------------------------------------|

### Building the AWS C++ SDK From Source

If you encounter problems during the SDK build via Bazel, you can attempt to build it from source (not recommended) and
comment-out the appropriate AWS rules in the Bazel package.

By following the rules in the
the [official docs](https://docs.aws.amazon.com/sdk-for-cpp/v1/developer-guide/setup-linux.html) and
the [Git repo](https://github.com/aws/aws-sdk-cpp), execute the following:

1. Install dependencies: `sudo apt-get install libcurl4-openssl-dev libssl-dev uuid-dev zlib1g-dev libpulse-dev`
2. Recursively clone the repo: `git clone --recurse-submodules https://github.com/aws/aws-sdk-cpp`
3. Create an out-of-source build directory: `mkdir build`
4.

Run: `cmake ../aws-sdk-cpp -DCMAKE_BUILD_TYPE=Release -DBUILD_ONLY="s3;rds" -DBUILD_SHARED_LIBS=ON -DENABLE_TESTING=OFF`

5. Run: `make && make install`

## Push Service Usage

Call `bazel run` as follows:

`bazel run //push-service:main`
