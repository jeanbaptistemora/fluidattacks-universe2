# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# https://github.com/fluidattacks/makes
{
  outputs,
  projectPath,
  ...
}: {
  imports = [
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
          outputs."/skims/env/type-stubs"
        ];
        mypyVersion = "0.971";
        python = "3.8";
        src = "/skims/skims";
      };
      skimsSca = {
        searchPaths.source = [
          outputs."/skims/config/runtime"
          outputs."/skims/env/type-stubs"
        ];
        mypyVersion = "0.971";
        python = "3.8";
        src = "/skims/sca/update";
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
        mypyVersion = "0.971";
        python = "3.8";
        src = "/skims/test";
      };
    };
  };
  secretsForAwsFromGitlab = {
    prodSkims = {
      roleArn = "arn:aws:iam::205810638802:role/prod_skims";
      duration = 3600;
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
