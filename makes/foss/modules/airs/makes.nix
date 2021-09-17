# https://github.com/fluidattacks/makes
{
  imports = [
    ./infra/makes.nix
    ./pipeline/makes.nix
  ];
  secretsForAwsFromEnv = {
    airsDev = {
      accessKeyId = "AIRS_DEV_AWS_ACCESS_KEY_ID";
      secretAccessKey = "AIRS_DEV_AWS_SECRET_ACCESS_KEY";
    };
    airsProd = {
      accessKeyId = "AIRS_PROD_AWS_ACCESS_KEY_ID";
      secretAccessKey = "AIRS_PROD_AWS_SECRET_ACCESS_KEY";
    };
  };
}
