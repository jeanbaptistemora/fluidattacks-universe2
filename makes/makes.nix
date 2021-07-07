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
  lintBash = {
    enable = true;
    targets = [ "/" ];
  };
  lintNix = {
    enable = true;
    targets = [ "/" ];
  };
}
