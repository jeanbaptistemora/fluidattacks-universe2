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
  secretsForAwsFromEnv = {
    prodObserves = {
      accessKeyId = "PROD_OBSERVES_AWS_ACCESS_KEY_ID";
      secretAccessKey = "PROD_OBSERVES_AWS_SECRET_ACCESS_KEY";
      sessionToken = "AWS_SESSION_TOKEN";
    };
  };
}
