{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      observes = {
        setup = [ outputs."/secretsForAwsFromEnv/prodObserves" ];
        src = "/makes/foss/modules/observes/infra/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      observes = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/makes/foss/modules/observes/infra/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      observes = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/makes/foss/modules/observes/infra/infra";
        version = "1.0";
      };
    };
  };
}
