# https://github.com/fluidattacks/makes
{ config
, ...
}:
{
  deployContainerImage = {
    enable = true;
    images = {
      makesProd = {
        src = config.inputs.product.makes-oci;
        registry = "registry.gitlab.com";
        tag = "fluidattacks/product/makes:latest";
      };
    };
  };
  formatBash = {
    enable = true;
    targets = [ "/" ];
  };
  formatNix = {
    enable = true;
    targets = [ "/" ];
  };
  formatPython = {
    enable = true;
    targets = [ "/" ];
  };
  formatTerraform = {
    enable = true;
    targets = [ "/" ];
  };
  lintBash = {
    enable = true;
    targets = [ "/" ];
  };
  lintNix = {
    enable = true;
    targets = [ "/" ];
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
    modules = {
      makesCi = {
        src = "/makes/applications/makes/ci/src/terraform";
        version = "0.13";
      };
    };
  };
}
