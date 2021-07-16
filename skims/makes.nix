# https://github.com/fluidattacks/makes
{ inputs
, ...
}:
{
  deployContainerImage = {
    enable = true;
    images = {
      skimsProd = {
        src = inputs.product.skims-oci-build;
        registry = "registry.gitlab.com";
        tag = "fluidattacks/product/skims:latest";
      };
    };
  };
  lintPython = {
    enable = true;
    modules = {
      skimsTestSdk = {
        extraSources = [
          inputs.product.skims-config-sdk
        ];
        python = "3.8";
        src = "/makes/applications/skims/test/sdk/src";
      };
    };
  };
}
