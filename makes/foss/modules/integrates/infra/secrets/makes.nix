{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      integratesSecrets = {
        setup = [ outputs."/secretsForAwsFromEnv/prodIntegrates" ];
        src = "/makes/foss/modules/integrates/infra/secrets/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesSecrets = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/makes/foss/modules/integrates/infra/secrets/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      integratesSecrets = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/makes/foss/modules/integrates/infra/secrets/infra";
        version = "1.0";
      };
    };
  };
}
