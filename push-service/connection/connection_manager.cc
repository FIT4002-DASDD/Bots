#include "connection_manager.h"

#include <cstdlib>
#include <memory>

#include "absl/memory/memory.h"
#include "absl/strings/str_format.h"
#include "aws/core/auth/AWSCredentials.h"
#include "aws/s3/S3Client.h"
#include "glog/logging.h"

namespace dasdd {
namespace {
using ::Aws::Auth::AWSCredentials;
using ::Aws::Client::ClientConfiguration;
using ::Aws::S3::S3Client;

std::unique_ptr<pqxx::connection> CreateRDSConnection() {
  const std::string host = std::getenv("DB_HOST");
  const std::string port = std::getenv("DB_PORT");
  const std::string name = std::getenv("DB_NAME");
  const std::string user = std::getenv("DB_USERNAME");
  const std::string password = std::getenv("DB_PASSWORD");

  std::unique_ptr<pqxx::connection> conn;
  try {
    conn = absl::make_unique<pqxx::connection>(
        absl::StrFormat("host=%s port=%s dbname=%s user=%s password=%s", host,
                        port, name, user, password));
  } catch (const std::exception& ex) {
    // DB connection errors should be non-fatal and we should just skip the
    // current upload cycle.
    LOG(ERROR) << absl::StrFormat("Connection to DB failed. Error: %s",
                                  ex.what());
  }
  return conn;
}

std::unique_ptr<S3Client> CreateS3Client() {
  const std::string region = std::getenv("AWS_REGION");
  const std::string access_key_id = std::getenv("AWS_ACCESS_KEY_ID");
  const std::string secret_key = std::getenv("AWS_SECRET_KEY");

  ClientConfiguration configuration;
  configuration.region = region;
  AWSCredentials credentials;
  credentials.SetAWSAccessKeyId(access_key_id);
  credentials.SetAWSSecretKey(secret_key);
  return absl::make_unique<S3Client>(credentials, configuration);
}

}  // namespace

ConnectionManager::ConnectionManager() {
  rds_connection_ = CreateRDSConnection();
  s3_client_ = CreateS3Client();
}

}  // namespace dasdd