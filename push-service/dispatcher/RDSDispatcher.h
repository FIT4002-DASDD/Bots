#ifndef PUSH_SERVICE_DISPATCHER_RDSDISPATCHER_H_
#define PUSH_SERVICE_DISPATCHER_RDSDISPATCHER_H_

#include <vector>

#include "absl/status/statusor.h"
#include "absl/synchronization/mutex.h"

class RDSDispatcher {
public:
  RDSDispatcher() = default;

  absl::StatusOr<bool> Dispatch() const;

  void AddToResultsBuffer() ABSL_LOCKS_EXCLUDED(mutex_);


private:
  std::vector<int> results_buffer ABSL_GUARDED_BY(mutex_);

  absl::Mutex mutex_;
};

#endif // PUSH_SERVICE_DISPATCHER_RDSDISPATCHER_H_
