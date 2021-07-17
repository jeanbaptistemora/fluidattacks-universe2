# https://github.com/fluidattacks/makes
{ inputs
, ...
}:
{
  deployContainerImage = {
    images = {
      skimsProd = {
        src = inputs.product.skims-oci-build;
        registry = "registry.gitlab.com";
        tag = "fluidattacks/product/skims:latest";
      };
    };
  };
  lintPython = {
    dirsOfModules = {
      skims = {
        extraSources = [
          inputs.product.skims-config-development
          inputs.product.skims-config-runtime
        ];
        python = "3.8";
        src = "/skims/skims";
      };
    };
    modules = {
      skimsTest = {
        extraSources = [
          inputs.product.skims-config-development
          inputs.product.skims-config-runtime
        ];
        python = "3.8";
        src = "/skims/test";
      };
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
