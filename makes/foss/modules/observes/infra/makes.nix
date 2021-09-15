{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      observes = {
        setup = [ outputs."/secretsForAwsFromEnv/observesProd" ];
        src = "/makes/foss/modules/observes/infra/infra";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      observes = {
        setup = [ outputs."/secretsForAwsFromEnv/observesDev" ];
        src = "/makes/foss/modules/observes/infra/infra";
        version = "0.14";
      };
    };
  };
  testTerraform = {
    modules = {
      observes = {
        setup = [ outputs."/secretsForAwsFromEnv/observesDev" ];
        src = "/makes/foss/modules/observes/infra/infra";
        version = "0.14";
      };
    };
  };
}
