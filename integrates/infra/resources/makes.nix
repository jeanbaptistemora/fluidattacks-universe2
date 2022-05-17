{outputs, ...}: {
  deployTerraform = {
    modules = {
      integratesResources = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodIntegrates"
        ];
        src = "/integrates/infra/resources/src";
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
        src = "/integrates/infra/resources/src";
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
        src = "/integrates/infra/resources/src";
        version = "1.0";
      };
    };
  };
}
