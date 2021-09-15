{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      integratesBackups = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesProd" ];
        src = "/makes/foss/modules/integrates/infra/backups/infra";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesBackups = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesDev" ];
        src = "/makes/foss/modules/integrates/infra/backups/infra";
        version = "0.14";
      };
    };
  };
  testTerraform = {
    modules = {
      integratesBackups = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesDev" ];
        src = "/makes/foss/modules/integrates/infra/backups/infra";
        version = "0.14";
      };
    };
  };
}
