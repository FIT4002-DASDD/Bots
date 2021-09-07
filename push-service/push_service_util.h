#ifndef PUSH_SERVICE_PUSH_SERVICE_UTIL_H_
#define PUSH_SERVICE_PUSH_SERVICE_UTIL_H_

#include <vector>

#include "absl/status/status.h"
#include "aws/s3/S3Client.h"
#include "pqxx/pqxx"
#include "proto/ad.pb.h"

namespace dasdd {

// Returns a list of paths to serialized protocol buffer binaries in a given
// directory.
std::vector<std::string> GetAllPathsToProtosInDirectory(
    const std::string& directory);

// Uploads a single AdCollection to AWS, including both S3 and RDS.
absl::Status UploadAdCollection(const dasdd::proto::AdCollection& ad_collection,
                                const Aws::S3::S3Client& client,
                                pqxx::connection& connection);

}  // namespace dasdd

#endif  // PUSH_SERVICE_PUSH_SERVICE_UTIL_H_