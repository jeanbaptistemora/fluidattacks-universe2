# https://github.com/fluidattacks/makes
{
  imports = [
    ./dev/makes.nix
    ./infra/makes.nix
    ./linters/makes.nix
    ./on-aws-batch/makes.nix
    ./pipeline/makes.nix
    ./security/makes.nix
  ];
  secretsForAwsFromEnv = {
    integratesProd = {
      accessKeyId = "INTEGRATES_PROD_AWS_ACCESS_KEY_ID";
      secretAccessKey = "INTEGRATES_PROD_AWS_SECRET_ACCESS_KEY";
    };
  };
}
