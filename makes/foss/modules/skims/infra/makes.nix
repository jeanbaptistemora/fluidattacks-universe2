# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployContainerImage = {
    images = {
      skimsProd = {
        src = outputs."/skims/container";
        registry = "registry.gitlab.com";
        tag = "fluidattacks/product/skims:latest";
      };
    };
  };
  deployTerraform = {
    modules = {
      skims = {
        setup = [ outputs."/secretsForAwsFromEnv/prodSkims" ];
        src = "/skims/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      skims = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/skims/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      skims = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/skims/infra";
        version = "1.0";
      };
    };
  };
}
