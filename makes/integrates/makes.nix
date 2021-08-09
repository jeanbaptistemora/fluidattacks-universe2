# https://github.com/fluidattacks/makes
{
  imports = [
    ./infra/makes.nix
    ./linters/makes.nix
    ./pipeline/makes.nix
  ];
  secretsForAwsFromEnv = {
    integratesDev = {
      accessKeyId = "INTEGRATES_DEV_AWS_ACCESS_KEY_ID";
      secretAccessKey = "INTEGRATES_DEV_AWS_SECRET_ACCESS_KEY";
    };
    integratesProd = {
      accessKeyId = "INTEGRATES_PROD_AWS_ACCESS_KEY_ID";
      secretAccessKey = "INTEGRATES_PROD_AWS_SECRET_ACCESS_KEY";
    };
  };
}
