# Provide a pkgs.stdenv.mkDerivation that has been patched with some
# boilerplate code common to all build processes we do in the repository

path: pkgs:

__attrs:
let
  nix = import (path "/makes/utils/nix") path pkgs;

  # Validate arguments
  attrs = builtins.mapAttrs
    (k: v: (
      if (
        (pkgs.lib.strings.hasPrefix "__env" k) ||
        (pkgs.lib.strings.hasPrefix "env" k) ||
        (k == "builder") ||
        (k == "buildInputs") ||
        (k == "name")
      )
      then v
      else abort "Invalid argument: ${k}, must be one of: builder, buildInputs, name, or start with: env or __env"
    ))
    __attrs;
in
pkgs.stdenv.mkDerivation (attrs // {
  __envBashLibCommon = path "/makes/utils/common/template.sh";
  __envBashLibShopts = path "/makes/utils/shopts/template.sh";
  __envStdenv = "${pkgs.stdenv}/setup";
  builder = builtins.toFile "setup-make-derivation" ''
    source $__envStdenv
    source $__envBashLibShopts
    source $__envBashLibCommon

    cd "$(mktemp -d)"

    ${nix.asContent attrs.builder}
  '';
})
