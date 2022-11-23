{
  inputs,
  libGit,
  makeScript,
  makeNodeJsEnvironment,
  ...
}: let
  name = "integrates-back-lint-schema";
  nodeJsEnvironment = makeNodeJsEnvironment {
    inherit name;
    nodeJsVersion = "14";
    packageJson = ./npm/package.json;
    packageLockJson = ./npm/package-lock.json;
  };
in
  makeScript {
    entrypoint = ./entrypoint.sh;
    inherit name;
    searchPaths = {
      bin = [
        inputs.nixpkgs.git
        inputs.nixpkgs.openssh
      ];
      source = [
        libGit
        nodeJsEnvironment
      ];
    };
  }
