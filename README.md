# FIT4002-DASDD-Bots

This is a project that consists of several subprojects that each make use of several technologies, including Python,
Node.JS, Protocol Buffers, and C++. As such, the [Bazel](https://bazel.build/) build system is used.

## Prerequisites

Install Bazel: https://docs.bazel.build/versions/main/install-ubuntu.html

## Running the E2E workflow

From the `scripts/` directory of the root project workspace, run the shell binary:
`./run-bots.sh`

This will spin up the bot workflow for all configured bots in the shell script in the **background**.

## Build Twitter Bots

From the root of the project workspace, run: `bazel build //bot:app`

## Running the Twitter Bots

There are several required flags to run the python binary. Please pass in the:

```shell
--bot_username=<username of the bot to be run>
--bot_password=<password of the bot to be run>
--bot_output_directory=<full path to the directory where bot output will be stored>
```

Note: for the `--bot_output_directory` flag, please pass in the path to the `bot_out` folder included in this workspace.

### Bots run example

Call `bazel run`, passing in the flags discussed above:

```shell
bazel run //bot:app -- --bot_username=Allison45555547 --bot_password=A2IHNDjPu23SNEjfy4ts --bot_output_directory=/home/akshay/Desktop/Uni/FIT4002/FIT4002-DASDD-Bots/bot_out
```

Or, alternatively, after building the `py_binary` target, execute it:

```shell
./bazel-bin/bot/app --bot_username=Allison45555547 --bot_password=A2IHNDjPu23SNEjfy4ts --bot_output_directory=/home/akshay/Desktop/Uni/FIT4002/FIT4002-DASDD-Bots/bot_out
```

### Debugging Bot output

The bots output results as serialized protocol buffer data (i.e. in binary format). This may be difficult to work with
when debugging. As such a utility in the form of a `py_binary` is provided to dump serialized data to the console and to
write out to a text proto.

Simply pass the path to the serialized proto as a value to the flag `--serialized_proto` when running
the `//bot/util:dump_proto` target. Example:

```shell
bazel run //bot/util:dump_proto -- --serialized_proto=/home/akshay/Desktop/Uni/FIT4002/FIT4002-DASDD-Bots/bot_out/akshay1738_2021-08-28_out
```

This will dump the data out to the console as well as write to a `textproto` file with the same name in the same
directory.

## Build Push Service

First install the AWS C++ SDK's dependencies by following
the [official docs](https://docs.aws.amazon.com/sdk-for-cpp/v1/developer-guide/setup-linux.html):

`sudo apt-get install libcurl4-openssl-dev libssl-dev uuid-dev zlib1g-dev libpulse-dev`.

Next install dependencies needed by libpqxx (a C++ Postgres binding), which should include installing Postgres
and `libpq` via a simple command such as: `sudo apt-get install -y libpq-dev`. See
this [repo](https://github.com/aksh0001/libpqxx-bazel) for more details.

Call `bazel build` on the `//push-service:main` target, specifying the full path to the Bazel cache directory in
the `--sandbox_writable_path` flag:

Example: `bazel build //push-service:main --sandbox_writable_path=/home/runner/.cache/bazel/`

| :exclamation: ** NOTE:** You must specify the `--sandbox_writable_path` when building. It is necessary as the AWS SDK's CMake rules make changes to the Bazel sandbox (which Bazel does not really like) - so this way we tell Bazel to expect that this directory will be changed. |
|-----------------------------------------|

### Building the AWS C++ SDK From Source

If you encounter problems during the SDK build via Bazel, you can attempt to build it from source (not recommended) and
comment-out the appropriate AWS rules in the Bazel package.

By following the rules in the
the [official docs](https://docs.aws.amazon.com/sdk-for-cpp/v1/developer-guide/setup-linux.html) and
the [Git repo](https://github.com/aws/aws-sdk-cpp), execute the following:

1. Install dependencies: `sudo apt-get install libcurl4-openssl-dev libssl-dev uuid-dev zlib1g-dev libpulse-dev`
2. Recursively clone the repo: `git clone --recurse-submodules https://github.com/aws/aws-sdk-cpp`
3. Create an out-of-source build directory: `mkdir build`
4. Run:
   ```bash
   cmake ../aws-sdk-cpp -DCMAKE_BUILD_TYPE=Release -DBUILD_ONLY="s3;rds" -DBUILD_SHARED_LIBS=ON -DENABLE_TESTING=OFF
   ```
5. Run: `make && make install`

## Push Service Usage

There are several environment variables, including secrets, needed to make it work. Please set the following:

```shell
# AWS RDS/Postgres variables:
export DB_HOST=<hostname of the db>
export DB_PORT=<port on which the db is listening on>
export DB_NAME=<name of the db>
export DB_USERNAME=<username to log into the db>
export DB_PASSWORD=<password to log into the db>
# AWS S3 variables:
export AWS_REGION=<region of bucket>
export AWS_ACCESS_KEY_ID=<aws access key id of an IAM user with appropriate permissions> 
export AWS_SECRET_KEY=<aws secret key of an IAM user with appropriate permissions>
```

In order for the Push Service to read generated Ad protocol buffer binaries from the bots, it needs to know where they
are stored. Pass the directory containing these protos as a `--bot_output_directory` flag to the binary.

To run it, call `bazel run` as follows:

```shell
bazel run //push-service:main -- --bot_output_directory=/home/akshay/Desktop/Uni/FIT4002/FIT4002-DASDD-Bots/bot_out
```

Or, alternatively, after building the `cc_binary` target, execute it:

```shell
./bazel-bin/push-service/main --bot_output_directory=/home/akshay/Desktop/Uni/FIT4002/FIT4002-DASDD-Bots/bot_out
```