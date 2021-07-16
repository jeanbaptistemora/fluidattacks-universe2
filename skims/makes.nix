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
      skimsTestMocksHttp = {
        extraSources = [
          inputs.product.skims-test-mocks-http-env
        ];
        python = "3.8";
        src = "/makes/applications/skims/test/mocks/http/src";
      };
      skimsTestSdk = {
        extraSources = [
          inputs.product.skims-config-sdk
        ];
        python = "3.8";
        src = "/makes/applications/skims/test/sdk/src";
      };
      skimsProcessGroup = {
        extraSources = [
          inputs.product.skims-config-runtime
        ];
        python = "3.8";
        src = "/makes/applications/skims/process-group/src";
      };
    };
  };
}
