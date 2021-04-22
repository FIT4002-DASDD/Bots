# Push Service

A multithreaded C++ service to collect bot data and upload to an AWS RDS Posgres instance on a schedule.

## Prerequisites


You will need a c++ compiler (e.g. `g++`), `cmake`, and `make`.
- the [https://packages.ubuntu.com/xenial/build-essential](`build-essential`) package may be used to install one or more of these dependencies collectively

## Installation

1. Ensure you are in the `push-service` directory
2. Create an out-of-source build directory and change into it: `mkdir build && cd build`
3. Run: `cmake ..`
4. Run: `make`
5. After this, the built binaries can be located in the `push-service/bin` directory

## Usage

1. Once the binaries have been built, change into the relevant directory: `cd push-service/bin`
2. Run the executable: `./push-service`
3. Run the tests: `./testlib`
