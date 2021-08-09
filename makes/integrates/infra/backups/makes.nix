{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      integratesBackups = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesProd" ];
        src = "/integrates/deploy/backup";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesBackups = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesDev" ];
        src = "/integrates/deploy/backup";
        version = "0.14";
      };
    };
  };
  testTerraform = {
    modules = {
      integratesBackups = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesDev" ];
        src = "/integrates/deploy/backup";
        version = "0.14";
      };
    };
  };
}
