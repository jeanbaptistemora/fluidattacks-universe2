{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      integratesResources = {
        setup = [
          outputs."/secretsForAwsFromEnv/integratesDev"
        ];
        src = "/makes/foss/modules/integrates/infra/resources/infra";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesResources = {
        setup = [
          outputs."/secretsForAwsFromEnv/integratesDev"
        ];
        src = "/makes/foss/modules/integrates/infra/resources/infra";
        version = "0.14";
      };
    };
  };
  testTerraform = {
    modules = {
      integratesResources = {
        setup = [
          outputs."/secretsForAwsFromEnv/integratesDev"
        ];
        src = "/makes/foss/modules/integrates/infra/resources/infra";
        version = "0.14";
      };
    };
  };
}
