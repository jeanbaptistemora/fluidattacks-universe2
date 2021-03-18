# Provide a pkgs.stdenv.mkDerivation that has been patched with some
# boilerplate code common to all build processes we do in the repository

path: pkgs:

{ arguments ? { }
, builder
, local ? false
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
  __envSearchPaths =
    if searchPaths == { }
    then "/dev/null"
    else import (path "/makes/utils/make-search-paths") path pkgs searchPaths;
  __envSearchPathsBase = pkgs.lib.strings.makeBinPath [ pkgs.coreutils ];
  args = [
    (builtins.toFile "make-derivation" ''
      source $__envBashLibShopts
      source $__envBashLibCommon
      export PATH=$__envSearchPathsBase
      source $__envSearchPaths

      ${nix.asContent builder}
    '')
  ];
  builder = "${pkgs.bash}/bin/bash";
  inherit name;
  system = "x86_64-linux";
} // pkgs.lib.optionalAttrs local {
  allowSubstitutes = false;
  preferLocalBuild = true;
})
