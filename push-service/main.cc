#include <cstdlib>

#include "absl/status/statusor.h"
#include "runner.h"

#include "absl/flags/parse.h"
#include "glog/logging.h"

#include "aws/core/Aws.h"

int main(int argc, char **argv) {
  // Must wait for Abseil integration with Google log.
  FLAGS_logtostderr = true;
  absl::ParseCommandLine(argc, argv);
  google::InitGoogleLogging(argv[0]);

  Aws::SDKOptions options;
  Aws::InitAPI(options);
  absl::StatusOr<bool> stat;
  {
    LOG(INFO) << "Configured AWS SDK. Starting service...";
    stat = dasdd::Run();
  }
  Aws::ShutdownAPI(options);
  return stat.ok() ? EXIT_SUCCESS : EXIT_FAILURE;
}