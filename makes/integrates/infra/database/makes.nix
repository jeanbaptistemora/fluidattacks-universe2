{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      integratesDatabase = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesProd" ];
        src = "/makes/integrates/infra/database/infra";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesDatabase = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesDev" ];
        src = "/makes/integrates/infra/database/infra";
        version = "0.14";
      };
    };
  };
  testTerraform = {
    modules = {
      integratesDatabase = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesDev" ];
        src = "/makes/integrates/infra/database/infra";
        version = "0.14";
      };
    };
  };
}
