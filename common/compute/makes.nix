# https://github.com/fluidattacks/makes
{outputs, ...}: {
  imports = [
    ./arch/makes.nix
    ./schedule/makes.nix
  ];
  deployTerraform = {
    modules = {
      commonCompute = {
        setup = [
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
          outputs."/common/compute/schedule/parse-terraform"
        ];
        src = "/common/compute/infra";
        version = "1.0";
      };
    };
  };
}
