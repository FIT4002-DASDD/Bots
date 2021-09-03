#include "runner.h"

#include <chrono>
#include <thread>
#include <vector>

#include "absl/base/attributes.h"
#include "absl/flags/flag.h"
#include "absl/strings/str_format.h"
#include "glog/logging.h"
#include "push_service_util.h"

ABSL_FLAG(uint64_t, cycle_time_minutes, 1,
          "Set the time for which the Push Service cycle repeats");

namespace dasdd {
namespace {
constexpr unsigned int kParallelThreadCount =
    5;  // Upto std::thread::hardware_concurrency() limit

void PrintWelcomeText() {
  LOG(INFO) << "Running Push Service...";
  LOG(INFO) << absl::StrFormat("Parallel thread count: %d",
                               kParallelThreadCount);
}

void Handler() {
  LOG(INFO) << "Thread id: " << std::this_thread::get_id();

  // Read the files n' extract the data
  // read()
  // Dispatch the data to AWS RDS
  // OR... buffer the dispatch.. e.g. in a vector so as to avoid several cycles
  // (will need locking around a std::vector?) dispatch()
}

ABSL_ATTRIBUTE_NORETURN void Dispatch() {
  std::vector<std::thread> threads;
  while (true) {
    for (unsigned int i = 0; i < kParallelThreadCount; i++) {
      std::thread t(Handler);
      threads.push_back(std::move(t));
    }
    for (std::thread &t : threads) {
      t.join();
    }

    LOG(INFO) << "Cycle finished. Sleeping until next cycle starts...";
    threads.clear();
    std::this_thread::sleep_for(
        std::chrono::minutes(absl::GetFlag(FLAGS_cycle_time_minutes)));
  }
}

}  // namespace

absl::StatusOr<bool> Run() {
  PrintWelcomeText();

  Dispatch();

  return absl::OkStatus();
}

}  // namespace dasdd