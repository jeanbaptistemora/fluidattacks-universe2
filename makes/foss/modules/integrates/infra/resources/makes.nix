{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      integratesResources = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodIntegrates"
        ];
        src = "/makes/foss/modules/integrates/infra/resources/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesResources = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
        ];
        src = "/makes/foss/modules/integrates/infra/resources/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      integratesResources = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
        ];
        src = "/makes/foss/modules/integrates/infra/resources/infra";
        version = "1.0";
      };
    };
  };
}
