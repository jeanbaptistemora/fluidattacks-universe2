{outputs, ...}: {
  deployTerraform = {
    modules = {
      integratesCache = {
        setup = [outputs."/secretsForAwsFromEnv/prodIntegrates"];
        src = "/integrates/infra/cache/src";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesCache = {
        setup = [outputs."/secretsForAwsFromEnv/dev"];
        src = "/integrates/infra/cache/src";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      integratesCache = {
        setup = [outputs."/secretsForAwsFromEnv/dev"];
        src = "/integrates/infra/cache/src";
        version = "1.0";
      };
    };
  };
}
