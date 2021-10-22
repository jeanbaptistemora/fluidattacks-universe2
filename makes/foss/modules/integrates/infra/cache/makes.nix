{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      integratesCache = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesProd" ];
        src = "/makes/foss/modules/integrates/infra/cache/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesCache = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/makes/foss/modules/integrates/infra/cache/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      integratesCache = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/makes/foss/modules/integrates/infra/cache/infra";
        version = "1.0";
      };
    };
  };
}
