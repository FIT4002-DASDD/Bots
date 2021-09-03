#ifndef PUSH_SERVICE_RUNNER_H_
#define PUSH_SERVICE_RUNNER_H_

#include "absl/status/statusor.h"

namespace dasdd {

absl::StatusOr<bool> Run();

}  // namespace dasdd

#endif  // PUSH_SERVICE_RUNNER_H_