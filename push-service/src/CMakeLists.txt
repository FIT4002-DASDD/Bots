set(HEADER_LIST_MODERN "${push-service_SOURCE_DIR}/include/modern/lib.h")

add_library(modern_library lib.cpp ${HEADER_LIST_MODERN})

target_include_directories(modern_library PUBLIC ../include)

target_compile_features(modern_library PUBLIC cxx_std_11)

source_group(
  TREE "${PROJECT_SOURCE_DIR}/include"
  PREFIX "Header Files"
  FILES ${HEADER_LIST})
