{
  imports = [
    ./infra/makes.nix
    ./linters/makes.nix
    ./pipeline/makes.nix
    ./tests/makes.nix
  ];
  secretsForAwsFromEnv = {
    sortsProd = {
      accessKeyId = "SORTS_PROD_AWS_ACCESS_KEY_ID";
      secretAccessKey = "SORTS_PROD_AWS_SECRET_ACCESS_KEY";
      sessionToken = "AWS_SESSION_TOKEN";
    };
  };
}
