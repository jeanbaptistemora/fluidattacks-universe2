pkgs:

rec {
  srcExternalDynamoDbLocal = pkgs.fetchurl {
    url = "https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_2020-05-19.zip";
    sha256 = "0lqxrbiqnvac8rq8x41pm76mb5bh4rxhfzj5yxji6n9q0m1wxbqq";
  };
}
