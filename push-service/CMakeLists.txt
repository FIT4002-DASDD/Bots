cmake_minimum_required(VERSION 3.11...3.20)

project(
        push-service
        VERSION 0.1
        DESCRIPTION "A CRON Worker to push bot data to AWS RDS and images to S3"
        LANGUAGES CXX)

if(CMAKE_PROJECT_NAME STREQUAL PROJECT_NAME)
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)

    set(CMAKE_CXX_EXTENSIONS OFF)

    set_property(GLOBAL PROPERTY USE_FOLDERS ON)

    include(CTest)

    find_package(Doxygen)
    if(Doxygen_FOUND)
        add_subdirectory(docs)
    else()
        message(STATUS "Doxygen not found, not building docs")
    endif()
endif()

include(FetchContent)
if(${CMAKE_VERSION} VERSION_LESS 3.14)
    include(cmake/add_FetchContent_MakeAvailable.cmake)
endif()

# Formatting library
FetchContent_Declare(
        fmtlib
        GIT_REPOSITORY https://github.com/fmtlib/fmt.git
        GIT_TAG 5.3.0)
FetchContent_MakeAvailable(fmtlib)

# AWS CPP SDK (todo)
#FetchContent_Declare(
#        aws-sdk-cpp
#        GIT_REPOSITORY "https://github.com/aws/aws-sdk-cpp"
#        GIT_TAG "1.8.14"
#        TEST_COMMAND ""
#        CMAKE_ARGS -DCMAKE_BUILD_TYPE=Debug
#                   -DBUILD_ONLY=s3
#                   -DBUILD_SHARED_LIBS=ON
#                   -DENABLE_TESTING=OFF
#)
#FetchContent_MakeAvailable(aws-sdk-cpp)

add_subdirectory(src)

add_subdirectory(apps)

if(CMAKE_PROJECT_NAME STREQUAL PROJECT_NAME)
    add_subdirectory(tests)
endif()