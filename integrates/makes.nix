# https://github.com/fluidattacks/makes
{
  imports = [
    ./back/lint/makes.nix
    ./dev/makes.nix
    ./infra/makes.nix
    ./on-aws-batch/makes.nix
    ./pipeline/makes.nix
    ./security/makes.nix
  ];
  secretsForAwsFromEnv = {
    prodIntegrates = {
      accessKeyId = "PROD_INTEGRATES_AWS_ACCESS_KEY_ID";
      secretAccessKey = "PROD_INTEGRATES_AWS_SECRET_ACCESS_KEY";
      sessionToken = "AWS_SESSION_TOKEN";
    };
  };
}
