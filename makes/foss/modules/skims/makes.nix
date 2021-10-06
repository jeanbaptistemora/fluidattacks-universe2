# https://github.com/fluidattacks/makes
{ inputs
, outputs
, ...
}:
{
  imports = [
    ./compute-on-aws-batch/makes.nix
    ./dev/makes.nix
    ./inputs/makes.nix
    ./tests/makes.nix
    ./pipeline/makes.nix
  ];
  deployContainerImage = {
    images = {
      skimsProd = {
        src = outputs."/skims/container";
        registry = "registry.gitlab.com";
        tag = "fluidattacks/product/skims:latest";
      };
    };
  };
  deployTerraform = {
    modules = {
      skims = {
        setup = [ outputs."/secretsForAwsFromEnv/skimsProd" ];
        src = "/skims/infra";
        version = "0.14";
      };
    };
  };
  lintPython = {
    dirsOfModules = {
      skims = {
        searchPaths.source = [
          inputs.product.skims-config-runtime
          outputs."/skims/env/development"
        ];
        python = "3.8";
        src = "/skims/skims";
      };
    };
    imports = {
      skims = {
        config = "/skims/setup.imports.cfg";
        src = "/skims/skims";
      };
    };
    modules = {
      skimsTest = {
        searchPaths.source = [
          inputs.product.skims-config-runtime
          outputs."/skims/env/development"
        ];
        python = "3.8";
        src = "/skims/test";
      };
      skimsTestMocksHttp = {
        searchPaths.source = [ outputs."/skims/test/mocks/http/env" ];
        python = "3.8";
        src = "/makes/foss/units/skims/test/mocks/http/src";
      };
      skimsTestSdk = {
        searchPaths.source = [
          inputs.product.skims-config-sdk
        ];
        python = "3.8";
        src = "/makes/foss/units/skims/test/sdk/src";
      };
      skimsProcessGroup = {
        searchPaths.source = [
          inputs.product.skims-config-runtime
        ];
        python = "3.8";
        src = "/makes/applications/skims/process-group/src";
      };
    };
  };
  lintTerraform = {
    modules = {
      skims = {
        setup = [ outputs."/secretsForAwsFromEnv/skimsDev" ];
        src = "/skims/infra";
        version = "0.14";
      };
    };
  };
  secretsForAwsFromEnv = {
    skimsDev = {
      accessKeyId = "SKIMS_DEV_AWS_ACCESS_KEY_ID";
      secretAccessKey = "SKIMS_DEV_AWS_SECRET_ACCESS_KEY";
    };
    skimsProd = {
      accessKeyId = "SKIMS_PROD_AWS_ACCESS_KEY_ID";
      secretAccessKey = "SKIMS_PROD_AWS_SECRET_ACCESS_KEY";
    };
  };
  securePythonWithBandit = {
    skims = {
      python = "3.8";
      target = "/skims/skims";
    };
  };
  testTerraform = {
    modules = {
      skims = {
        setup = [ outputs."/secretsForAwsFromEnv/skimsDev" ];
        src = "/skims/infra";
        version = "0.14";
      };
    };
  };
}
