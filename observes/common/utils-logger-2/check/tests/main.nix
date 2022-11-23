{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.common.utils_logger_2.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs;
  check = pkg.check.tests;
in
  makeScript {
    searchPaths = {
      bin = [check];
    };
    name = "observes-common-utils-logger-2-check-tests";
    entrypoint = "";
  }
