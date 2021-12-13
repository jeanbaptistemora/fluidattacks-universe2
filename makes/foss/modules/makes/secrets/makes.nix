# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesSecrets = {
        setup = [ outputs."/secretsForAwsFromEnv/prodMakes" ];
        src = "/makes/foss/modules/makes/secrets/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesSecrets = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/makes/foss/modules/makes/secrets/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      makesSecrets = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/makes/foss/modules/makes/secrets/infra";
        version = "1.0";
      };
    };
  };
}
