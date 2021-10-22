{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      integratesDatabase = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesProd" ];
        src = "/makes/foss/modules/integrates/infra/database/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesDatabase = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/makes/foss/modules/integrates/infra/database/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      integratesDatabase = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/makes/foss/modules/integrates/infra/database/infra";
        version = "1.0";
      };
    };
  };
}
