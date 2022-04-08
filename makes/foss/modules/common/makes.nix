# https://github.com/fluidattacks/makes
{
  imports = [
    ./ci/makes.nix
    ./compute/makes.nix
    ./criteria/makes.nix
    ./dns/makes.nix
    ./foss/makes.nix
    ./kubernetes/makes.nix
    ./okta/makes.nix
    ./pipeline/makes.nix
    ./status/makes.nix
    ./users/makes.nix
    ./vpc/makes.nix
    ./vpn/makes.nix
  ];
  secretsForAwsFromEnv = {
    dev = {
      accessKeyId = "DEV_AWS_ACCESS_KEY_ID";
      secretAccessKey = "DEV_AWS_SECRET_ACCESS_KEY";
      sessionToken = "AWS_SESSION_TOKEN";
    };
    prodCommon = {
      accessKeyId = "PROD_COMMON_AWS_ACCESS_KEY_ID";
      secretAccessKey = "PROD_COMMON_AWS_SECRET_ACCESS_KEY";
      sessionToken = "AWS_SESSION_TOKEN";
    };
  };
}
