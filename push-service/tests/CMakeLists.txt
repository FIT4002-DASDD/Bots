FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG master)
FetchContent_MakeAvailable(googletest)

add_executable(testlib testlib.cpp)

target_compile_features(testlib PRIVATE cxx_std_17)

# Should be linked to the main library, as well as the googletest testing library
target_link_libraries(testlib PRIVATE modern_library gtest_main)

# If you register a test, then ctest and make test will run it.
# You can also run examples and check the output, as well.
add_test(NAME testlibtest COMMAND testlib) # Command can be a target
