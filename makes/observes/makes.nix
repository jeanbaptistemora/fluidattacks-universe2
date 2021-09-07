{
  imports = [
    ./common/paginator/makes.nix
    ./infra/makes.nix
    ./linters/makes.nix
    ./pipeline/makes.nix
  ];
  secretsForAwsFromEnv = {
    observesDev = {
      accessKeyId = "OBSERVES_DEV_AWS_ACCESS_KEY_ID";
      secretAccessKey = "OBSERVES_DEV_AWS_SECRET_ACCESS_KEY";
    };
    observesProd = {
      accessKeyId = "OBSERVES_PROD_AWS_ACCESS_KEY_ID";
      secretAccessKey = "OBSERVES_PROD_AWS_SECRET_ACCESS_KEY";
    };
  };
}
