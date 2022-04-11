{outputs, ...}: {
  deployTerraform = {
    modules = {
      integratesDatabase = {
        setup = [outputs."/secretsForAwsFromEnv/prodIntegrates"];
        src = "/integrates/infra/database/src";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesDatabase = {
        setup = [outputs."/secretsForAwsFromEnv/dev"];
        src = "/integrates/infra/database/src";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      integratesDatabase = {
        setup = [outputs."/secretsForAwsFromEnv/dev"];
        src = "/integrates/infra/database/src";
        version = "1.0";
      };
    };
  };
}
