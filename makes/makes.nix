# https://github.com/fluidattacks/makes
{ config
, ...
}:
{
  deployContainerImage = {
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
    modules = {
      makesCi = {
        src = "/makes/applications/makes/ci/src/terraform";
        version = "0.13";
      };
    };
  };
}
