#include "runner.h"

#include <chrono>
#include <fstream>
#include <thread>
#include <vector>

#include "absl/base/attributes.h"
#include "absl/flags/flag.h"
#include "absl/strings/str_format.h"
#include "glog/logging.h"
#include "pqxx/pqxx"
#include "proto/ad.pb.h"
#include "push-service/connection/connection_manager.h"
#include "push-service/push_service_util.h"

ABSL_FLAG(uint64_t, cycle_time_minutes, 600,
          "Set the time for which the Push Service cycle repeats");

ABSL_FLAG(std::string, bot_output_directory, "",
          "Pass in the path to the bot output proto directory.");

namespace dasdd {
namespace {
using ::dasdd::proto::AdCollection;

// To be used when implementing thread pool.
constexpr unsigned int kParallelThreadCount =
    4;  // Upto std::thread::hardware_concurrency() limit

void PrintWelcomeText() {
  LOG(INFO) << "Running Push Service...";
  LOG(INFO) << absl::StrFormat("Parallel thread count: %d",
                               kParallelThreadCount);
}

ABSL_ATTRIBUTE_NORETURN void Dispatch() {
  while (true) {
    ConnectionManager cm;

    std::vector<std::string> proto_paths = GetAllPathsToProtosInDirectory(
        absl::GetFlag(FLAGS_bot_output_directory));
    for (const std::string& path : proto_paths) {
      if (cm.rds_connection()) {
        std::ifstream ifstream(path, std::ios::in | std::ios::binary);
        AdCollection ad_collection;
        ad_collection.ParseFromIstream(&ifstream);
        auto upload_status = UploadAdCollection(ad_collection, cm.s3_client(),
                                                *cm.rds_connection());
        if (!upload_status.ok()) {
          LOG(ERROR) << absl::StrFormat(
              "Unable to upload this AdCollection. Error: %s",
              upload_status.message());
        } else {
          // We're done with uploading the current proto; it can be deleted.
          std::filesystem::remove(path);
        }
      }
    }
    LOG(INFO) << "Cycle finished. Sleeping until next cycle starts...";
    std::this_thread::sleep_for(
        std::chrono::minutes(absl::GetFlag(FLAGS_cycle_time_minutes)));
  }
}

}  // namespace

absl::StatusOr<bool> Run() {
  PrintWelcomeText();

  Dispatch();

  return true;
}

}  // namespace dasdd