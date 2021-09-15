{
  imports = [
    ./infra/makes.nix
    ./linters/makes.nix
    ./pipeline/makes.nix
  ];
  secretsForAwsFromEnv = {
    sortsDev = {
      accessKeyId = "SORTS_DEV_AWS_ACCESS_KEY_ID";
      secretAccessKey = "SORTS_DEV_AWS_SECRET_ACCESS_KEY";
    };
    sortsProd = {
      accessKeyId = "SORTS_PROD_AWS_ACCESS_KEY_ID";
      secretAccessKey = "SORTS_PROD_AWS_SECRET_ACCESS_KEY";
    };
  };
}
