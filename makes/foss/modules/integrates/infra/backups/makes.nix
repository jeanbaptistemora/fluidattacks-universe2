{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      integratesBackups = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesProd" ];
        src = "/makes/foss/modules/integrates/infra/backups/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesBackups = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/makes/foss/modules/integrates/infra/backups/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      integratesBackups = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/makes/foss/modules/integrates/infra/backups/infra";
        version = "1.0";
      };
    };
  };
}
