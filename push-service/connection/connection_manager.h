#ifndef PUSH_SERVICE_CONNECTION_CONNECTION_MANAGER_H_
#define PUSH_SERVICE_CONNECTION_CONNECTION_MANAGER_H_

#include <memory>

#include "absl/base/attributes.h"
#include "aws/s3/S3Client.h"
#include "pqxx/pqxx"

namespace dasdd {
// A wrapper around RDS and S3 connections.
// Separate instances of this class should be used for each upload cycle; as we
// don't want a DB failure to be fatal to the entire application, using separate
// instances ensures that a new connection is opened and closed for each upload
// cycle via RAII.
class ConnectionManager {
 public:
  ConnectionManager();

  ABSL_MUST_USE_RESULT pqxx::connection* rds_connection() const {
    return rds_connection_.get();
  }
  ABSL_MUST_USE_RESULT Aws::S3::S3Client& s3_client() const {
    return *s3_client_;
  }

  ConnectionManager(const ConnectionManager& other) = delete;
  ConnectionManager& operator=(const ConnectionManager& other) = delete;

 private:
  std::unique_ptr<pqxx::connection> rds_connection_;
  std::unique_ptr<Aws::S3::S3Client> s3_client_;
};
}  // namespace dasdd

#endif  // PUSH_SERVICE_CONNECTION_CONNECTION_MANAGER_H_