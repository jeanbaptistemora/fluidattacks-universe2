# For more information visit:
# https://github.com/fluidattacks/makes
{
  imports = [
    ./forces/makes.nix
    ./integrates/makes.nix
    ./makes/makes.nix
    ./skims/makes.nix
  ];
  inputs = {
    product = import ./.;
  };
  cache = {
    enable = true;
    name = "fluidattacks";
    pubKey = "fluidattacks.cachix.org-1:upiUCP8kWnr7NxVSJtTOM+SBqL0pZhZnUoqPG04sBv0=";
  };
  lintTerraform = {
    enable = true;
    config = ''
      config {
        module = true
      }
      plugin "aws" {
        enabled = true
        deep_check = true
      }
      rule "aws_resource_missing_tags" {
        enabled = true
        tags = [
          "Name",
          "management:type",
          "management:product",
        ]
        exclude = [
          "aws_iam_policy",
        ]
      }
    '';
  };
  requiredMakesVersion = "21.08";
}
