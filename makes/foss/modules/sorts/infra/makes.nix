{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      sorts = {
        setup = [ outputs."/secretsForAwsFromEnv/sortsDev" ];
        src = "/makes/foss/modules/sorts/infra/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      sorts = {
        setup = [ outputs."/secretsForAwsFromEnv/sortsDev" ];
        src = "/makes/foss/modules/sorts/infra/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      sorts = {
        setup = [ outputs."/secretsForAwsFromEnv/sortsDev" ];
        src = "/makes/foss/modules/sorts/infra/infra";
        version = "1.0";
      };
    };
  };
}
