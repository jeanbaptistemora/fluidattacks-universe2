{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      observes = {
        setup = [ outputs."/secretsForAwsFromEnv/observesProd" ];
        src = "/makes/foss/modules/observes/infra/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      observes = {
        setup = [ outputs."/secretsForAwsFromEnv/observesDev" ];
        src = "/makes/foss/modules/observes/infra/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      observes = {
        setup = [ outputs."/secretsForAwsFromEnv/observesDev" ];
        src = "/makes/foss/modules/observes/infra/infra";
        version = "1.0";
      };
    };
  };
}
