{
  imports = [
    ./infra/makes.nix
    ./linters/makes.nix
    ./pipeline/makes.nix
    ./tests/makes.nix
  ];
  secretsForAwsFromEnv = {
    prodSorts = {
      accessKeyId = "PROD_SORTS_AWS_ACCESS_KEY_ID";
      secretAccessKey = "PROD_SORTS_AWS_SECRET_ACCESS_KEY";
      sessionToken = "AWS_SESSION_TOKEN";
    };
  };
}
