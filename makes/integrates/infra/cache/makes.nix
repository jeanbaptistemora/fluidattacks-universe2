{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      integratesCache = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesProd" ];
        src = "/makes/integrates/infra/cache/infra";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesCache = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesDev" ];
        src = "/makes/integrates/infra/cache/infra";
        version = "0.14";
      };
    };
  };
  testTerraform = {
    modules = {
      integratesCache = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesDev" ];
        src = "/makes/integrates/infra/cache/infra";
        version = "0.14";
      };
    };
  };
}
