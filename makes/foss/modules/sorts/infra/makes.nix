{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      sorts = {
        setup = [ outputs."/secretsForAwsFromEnv/sortsProd" ];
        src = "/makes/foss/modules/sorts/infra/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      sorts = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/makes/foss/modules/sorts/infra/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      sorts = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/makes/foss/modules/sorts/infra/infra";
        version = "1.0";
      };
    };
  };
}
