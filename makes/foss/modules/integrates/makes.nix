# https://github.com/fluidattacks/makes
{ outputs
, projectPath
, ...
}:
{
  imports = [
    ./dev/makes.nix
    ./infra/makes.nix
    ./linters/makes.nix
    ./on-aws-batch/makes.nix
    ./pipeline/makes.nix
    ./security/makes.nix
  ];
  dynamoDb = {
    integrates = {
      host = "127.0.0.1";
      port = "8022";
      daemonMode = false;
      infra = projectPath "/makes/foss/units/integrates/db/infra/";
      dataDerivation = [
        (outputs."/integrates/db/transformation")
      ];
    };
  };
  secretsForAwsFromEnv = {
    integratesProd = {
      accessKeyId = "INTEGRATES_PROD_AWS_ACCESS_KEY_ID";
      secretAccessKey = "INTEGRATES_PROD_AWS_SECRET_ACCESS_KEY";
    };
  };
}
