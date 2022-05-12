# https://github.com/fluidattacks/makes
{outputs, ...}: {
  imports = [
    ./schedule/makes.nix
  ];
  deployTerraform = {
    modules = {
      commonCompute = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodCommon"
          outputs."/common/compute/schedule/parse-terraform"
        ];
        src = "/common/compute/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonCompute = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/common/compute/schedule/parse-terraform"
        ];
        src = "/common/compute/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      commonCompute = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/common/compute/schedule/parse-terraform"
        ];
        src = "/common/compute/infra";
        version = "1.0";
      };
    };
  };
}
