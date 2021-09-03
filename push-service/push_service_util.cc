#include "push_service_util.h"

#include <fstream>
#include <iostream>

#include "absl/status/statusor.h"
#include "aws/s3/S3Client.h"
#include "aws/s3/model/PutObjectRequest.h"
#include "aws/core/auth/AWSCredentials.h"
#include "proto/ad.pb.h"
#include "proto/bot.pb.h"

namespace dasdd {
namespace {
using dasdd::proto::Ad;
using dasdd::proto::AdCollection;
using dasdd::proto::Bot;

constexpr char kBucketName[] = "dasdd-dev-stack-dasddadimagesstaging-1jz4qtcqsz6p3";
constexpr char kRegion[] = "ap-southeast-2";

}  // namespace

absl::StatusOr<bool> UploadAdCollection() {
  //  for (const Ad& ad : ad_collection.ads()) {
  //    // TODO
  //  }
  //  return true;

  Aws::Client::ClientConfiguration config;
  config.region = "ap-southeast-2";

  Aws::Auth::AWSCredentials credentials;
  credentials.SetAWSAccessKeyId("AKIATEGVOVNXRPZEMTOT");
  credentials.SetAWSSecretKey("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");

  Aws::S3::S3Client s3_client(credentials, config);


  Aws::S3::Model::PutObjectRequest request;
  request.SetBucket(kBucketName);
  request.SetKey("push_service_util.h");

  std::shared_ptr<Aws::IOStream> input_data =
      Aws::MakeShared<Aws::FStream>("SampleAllocationTag", "./push_service_util.h",
                                    std::ios_base::in | std::ios_base::binary);

  request.SetBody(input_data);


  Aws::S3::Model::PutObjectOutcome outcome = s3_client.PutObject(request);
  if (outcome.IsSuccess()) {
    std::cout << "Added object '"
              << "' to bucket '" << kBucketName << "'.";
    return true;
  } else {
    std::cout << "Error: PutObject: " << outcome.GetError().GetMessage()
              << std::endl;

    return false;
  }
}

}  // namespace dasdd