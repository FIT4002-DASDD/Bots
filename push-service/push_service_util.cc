#include "push_service_util.h"

#include <filesystem>
#include <iostream>
#include <regex>
#include <string>
#include <vector>

#include "absl/base/attributes.h"
#include "absl/status/status.h"
#include "absl/strings/str_format.h"
#include "aws/core/auth/AWSCredentials.h"
#include "aws/s3/S3Client.h"
#include "aws/s3/model/PutObjectRequest.h"
#include "glog/logging.h"
#include "google/protobuf/util/time_util.h"
#include "pqxx/pqxx"
#include "proto/ad.pb.h"
#include "proto/bot.pb.h"

namespace dasdd {
namespace {
using ::Aws::S3::S3Client;
using ::dasdd::proto::Ad;
using ::dasdd::proto::AdCollection;
using ::dasdd::proto::Bot;
using ::google::protobuf::util::TimeUtil;

constexpr char kTwitterAdTableName[] = "twitter_ad_test";
constexpr char kBucketName[] =
    "dasdd-dev-stack-dasddadimagesstaging-1jz4qtcqsz6p3";

// Constructs an INSERT query to insert an Ad's data into the Twitter Ad table.
std::string ConstructAdInsertQuery(const Ad& ad, const pqxx::work& w) {
  return absl::StrFormat(
      "INSERT INTO %s (\"promoterHandle\",\"content\","
      "\"officialLink\",\"tweetLink\",\"adType\") "
      "VALUES ('%s', '%s', '%s', '%s', '%s') "
      "ON CONFLICT DO NOTHING;",
      kTwitterAdTableName, w.esc(ad.promoter_handle()), w.esc(ad.content()),
      w.esc(ad.official_ad_link()), w.esc(ad.seen_on()),
      w.esc(Ad::AdType_Name(ad.ad_type())));
}

// Uploads a given image (in bytestring) format to S3 and returns its URL.
// The object_name is the filename of the resulting image in S3.
ABSL_MUST_USE_RESULT std::string UploadAdImage(
    const std::string& image_bytestring, const std::string& object_name,
    const S3Client& client) {
  if (image_bytestring.empty()) {
    return "";
  }

  Aws::S3::Model::PutObjectRequest request;
  request.SetBucket(kBucketName);
  request.SetKey(object_name);

  const auto input_data = Aws::MakeShared<Aws::StringStream>("");
  *input_data << image_bytestring;
  request.SetBody(input_data);

  Aws::S3::Model::PutObjectOutcome outcome = client.PutObject(request);
  if (!outcome.IsSuccess()) {
    LOG(ERROR) << "Failed to upload Ad image to S3.";
    return "";
  }
  // TODO: Verify this URL.
  return absl::StrFormat("https://%s.ap-southeast-2/%s", kBucketName,
                         object_name);
}

}  // namespace

absl::Status UploadAdCollection(const AdCollection& ad_collection,
                                const S3Client& client,
                                pqxx::connection& connection) {
  CHECK(connection.is_open());

  for (const Ad& ad : ad_collection.ads()) {
    // Upload any images associated with this Ad to S3.
    const std::string image_name =
        absl::StrFormat("%s_%s.png", ad_collection.bot().id(),
                        TimeUtil::ToString(ad.created_at()));
    const std::string screenshot_s3_url =
        UploadAdImage(ad.screenshot(), image_name, client);

    // Upload the rest of the Ad to RDS.
    try {
      pqxx::work w(connection);
      w.exec(ConstructAdInsertQuery(ad, w));
      w.commit();
    } catch (const std::exception& ex) {
      return absl::InternalError(
          absl::StrFormat("Push to RDS failed. Error: %s", ex.what()));
    }
  }

  LOG(INFO) << absl::StrFormat("Successful upload of AdCollection for Bot: %s.",
                               ad_collection.bot().id());
  return absl::OkStatus();
}

std::vector<std::string> GetAllPathsToProtosInDirectory(
    const std::string& directory) {
  const std::regex proto_file_regex("^.*?_out$");
  std::vector<std::string> paths;
  for (const auto& entry : std::filesystem::directory_iterator(directory)) {
    if (std::regex_match(entry.path().string(), proto_file_regex)) {
      paths.push_back(entry.path().string());
    }
  }
  return paths;
}

}  // namespace dasdd