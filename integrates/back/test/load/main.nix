{
  inputs,
  libGit,
  makeNodeJsModules,
  makeScript,
  projectPath,
  ...
}: let
  runtime = makeNodeJsModules {
    name = "integrates-back-test-load-runtime";
    nodeJsVersion = "18";
    packageJson = projectPath "/integrates/back/test/load/package.json";
    packageLockJson = projectPath "/integrates/back/test/load/package-lock.json";
  };
in
  makeScript {
    entrypoint = ./entrypoint.sh;
    name = "integrates-back-test-load";
    replace = {
      __argRuntime__ = runtime;
    };
    searchPaths = {
      bin = [
        inputs.nixpkgs.bash
        inputs.nixpkgs.k6
        inputs.nixpkgs.nodejs-18_x
      ];
      source = [
        libGit
      ];
    };
  }
