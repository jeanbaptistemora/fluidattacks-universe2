# https://github.com/fluidattacks/makes
{
  imports = [
    ./back/makes.nix
    ./infra/makes.nix
    ./pipeline/makes.nix
    ./jobs/makes.nix
    ./streams/makes.nix
  ];
  secretsForAwsFromGitlab = {
    prodIntegrates = {
      roleArn = "arn:aws:iam::205810638802:role/prod_integrates";
      duration = 3600;
    };
  };
}
