#ifndef PUSH_SERVICE_PUSH_SERVICE_UTIL_H_
#define PUSH_SERVICE_PUSH_SERVICE_UTIL_H_

#include "absl/status/statusor.h"
#include "proto/ad.pb.h"

namespace dasdd {

absl::StatusOr<bool> UploadAdCollection();

//absl::StatusOr<bool> UploadAdCollection(
//    const dasdd::proto::AdCollection& ad_collection);

}  // namespace dasdd

#endif  // PUSH_SERVICE_PUSH_SERVICE_UTIL_H_