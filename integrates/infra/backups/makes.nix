{outputs, ...}: {
  deployTerraform = {
    modules = {
      integratesBackups = {
        setup = [outputs."/secretsForAwsFromEnv/prodIntegrates"];
        src = "/integrates/infra/backups/src";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesBackups = {
        setup = [outputs."/secretsForAwsFromEnv/dev"];
        src = "/integrates/infra/backups/src";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      integratesBackups = {
        setup = [outputs."/secretsForAwsFromEnv/dev"];
        src = "/integrates/infra/backups/src";
        version = "1.0";
      };
    };
  };
}
