# https://github.com/fluidattacks/makes
{
  outputs,
  projectPath,
  ...
}: {
  imports = [
    ./batch/makes.nix
    ./dev/makes.nix
    ./infra/makes.nix
    ./inputs/makes.nix
    ./test/makes.nix
    ./pipeline/makes.nix
  ];
  inputs = {
    observesIndex = import (projectPath "/observes/architecture/index.nix");
  };
  lintPython = {
    dirsOfModules = {
      skims = {
        searchPaths.source = [
          outputs."/skims/config/runtime"
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
          outputs."/skims/config/runtime"
          outputs."/skims/env/development"
        ];
        python = "3.8";
        src = "/skims/test";
      };
      skimsTestMocksHttp = {
        searchPaths.source = [outputs."/skims/test/mocks/http/env"];
        python = "3.8";
        src = "/skims/test/mocks/http/src";
      };
    };
  };
  secretsForAwsFromEnv = {
    prodSkims = {
      accessKeyId = "PROD_SKIMS_AWS_ACCESS_KEY_ID";
      secretAccessKey = "PROD_SKIMS_AWS_SECRET_ACCESS_KEY";
      sessionToken = "AWS_SESSION_TOKEN";
    };
  };
  securePythonWithBandit = {
    skims = {
      python = "3.8";
      target = "/skims/skims";
    };
  };
  dynamoDb = {
    skims = {
      host = "127.0.0.1";
      port = "8022";
      infra = projectPath "/integrates/db/infra";
      data = [
        (projectPath "/skims/test/data/db")
      ];
    };
  };
}
