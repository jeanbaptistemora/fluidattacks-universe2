# https://github.com/fluidattacks/makes
{ config
, ...
}:
{
  deployContainerImage = {
    enable = true;
    images = {
      skimsProd = {
        src = config.inputs.product.skims-oci-build;
        registry = "registry.gitlab.com";
        tag = "fluidattacks/product/skims:latest";
      };
    };
  };
}
