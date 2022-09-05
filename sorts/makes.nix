{
  imports = [
    ./dev/makes.nix
    ./infra/makes.nix
    ./lint/makes.nix
    ./pipeline/makes.nix
    ./test/makes.nix
  ];
  secretsForAwsFromGitlab = {
    prodSorts = {
      roleArn = "arn:aws:iam::205810638802:role/prod_sorts";
      duration = 3600;
    };
  };
}
