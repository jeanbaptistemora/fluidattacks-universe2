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
        outputs."/integrates/db/transformation"
      ];
    };
  };
  secretsForAwsFromEnv = {
    prodIntegrates = {
      accessKeyId = "PROD_INTEGRATES_AWS_ACCESS_KEY_ID";
      secretAccessKey = "PROD_INTEGRATES_AWS_SECRET_ACCESS_KEY";
      sessionToken = "AWS_SESSION_TOKEN";
    };
  };
}
