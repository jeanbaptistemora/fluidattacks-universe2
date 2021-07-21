# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesSecrets = {
        setup = [ outputs."/secretsForAwsFromEnv/makesProd" ];
        src = "/makes/makes/secrets/infra";
        version = "0.13";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesSecrets = {
        setup = [ outputs."/secretsForAwsFromEnv/makesDev" ];
        src = "/makes/makes/secrets/infra";
        version = "0.13";
      };
    };
  };
  testTerraform = {
    modules = {
      makesSecrets = {
        setup = [ outputs."/secretsForAwsFromEnv/makesDev" ];
        src = "/makes/makes/secrets/infra";
        version = "0.13";
      };
    };
  };
}
