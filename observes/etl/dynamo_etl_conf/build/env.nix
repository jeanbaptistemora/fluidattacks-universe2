{
  lib,
  pythonPkgs,
  src,
  env,
}: let
  args = {inherit lib pythonPkgs src;};
  self = (import ./pkg/default.nix args)."${env}";
in
  lib.buildEnv.override {
    extraLibs = [self];
    ignoreCollisions = false;
  }
