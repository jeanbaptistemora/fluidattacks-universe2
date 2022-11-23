{projectPath, ...}: {
  imports = [
    ./batch/makes.nix
    ./dev/makes.nix
    ./infra/makes.nix
    ./lint/makes.nix
    ./pipeline/makes.nix
  ];
  inputs = {
    observesIndex = import (projectPath "/observes/architecture/index.nix");
  };
  secretsForAwsFromGitlab = {
    prodObserves = {
      roleArn = "arn:aws:iam::205810638802:role/prod_observes";
      duration = 3600;
    };
  };
}
