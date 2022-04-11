{outputs, ...}: {
  deployTerraform = {
    modules = {
      sorts = {
        setup = [outputs."/secretsForAwsFromEnv/prodSorts"];
        src = "/sorts/infra/src";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      sorts = {
        setup = [outputs."/secretsForAwsFromEnv/dev"];
        src = "/sorts/infra/src";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      sorts = {
        setup = [outputs."/secretsForAwsFromEnv/dev"];
        src = "/sorts/infra/src";
        version = "1.0";
      };
    };
  };
}
