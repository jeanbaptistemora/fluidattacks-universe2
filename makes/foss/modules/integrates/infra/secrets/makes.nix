{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      integratesSecrets = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesProd" ];
        src = "/makes/foss/modules/integrates/infra/secrets/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesSecrets = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesDev" ];
        src = "/makes/foss/modules/integrates/infra/secrets/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      integratesSecrets = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesDev" ];
        src = "/makes/foss/modules/integrates/infra/secrets/infra";
        version = "1.0";
      };
    };
  };
}
