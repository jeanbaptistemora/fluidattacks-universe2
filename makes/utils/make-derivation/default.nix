# Provide a pkgs.stdenv.mkDerivation that has been patched with some
# boilerplate code common to all build processes we do in the repository

path: pkgs:

{ arguments ? { }
, builder
, name
, searchPaths ? { }
}:
let
  nix = import (path "/makes/utils/nix") path pkgs;

  # Validate arguments
  arguments' = builtins.mapAttrs
    (k: v: (
      if (
        (pkgs.lib.strings.hasPrefix "__env" k) ||
        (pkgs.lib.strings.hasPrefix "env" k)
      )
      then v
      else abort "Invalid argument: ${k}, must start with: env or __env"
    ))
    arguments;
in
builtins.derivation (arguments' // {
  __envBashLibCommon = path "/makes/utils/common/template.sh";
  __envBashLibShopts = path "/makes/utils/shopts/template.sh";
  __envSeachPaths =
    if searchPaths == { }
    then "/dev/null"
    else import (path "/makes/utils/make-search-paths") path pkgs searchPaths;
  __envSeachPathsBase = pkgs.lib.strings.makeBinPath [
    pkgs.coreutils
    pkgs.gnugrep
    pkgs.gnused
  ];
  args = [
    (builtins.toFile "make-derivation" ''
      source $__envBashLibShopts
      source $__envBashLibCommon
      export PATH=$__envSeachPathsBase
      source $__envSeachPaths

      cd "$(mktemp -d)"

      ${nix.asContent builder}
    '')
  ];
  builder = "${pkgs.bash}/bin/bash";
  inherit name;
  system = "x86_64-linux";
})
