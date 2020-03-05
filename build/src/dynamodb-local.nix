pkgs:

rec {
  srcExternalDynamoDbLocal = pkgs.fetchurl {
    url = "https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.zip";
    sha256 = "0crca9j5mizxl3iqbgmfs1vj7hxpxzqgnd75jc3c7v836ydl86zm";
  };
}
