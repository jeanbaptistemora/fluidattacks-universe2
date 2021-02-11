# Replace arguments in the template

path: pkgs:

{ arguments
, name
, template
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path pkgs;
  nix = import (path "/makes/utils/nix") path pkgs;

  argumentNames = builtins.attrNames arguments;
  argumentNamesFile = builtins.toFile "arguments" (
    if builtins.length argumentNames > 0
    then builtins.concatStringsSep "\n" (argumentNames ++ [ "" ])
    else ""
  );

  # Validate arguments
  arguments' = builtins.mapAttrs
    (k: v: (
      if pkgs.lib.strings.hasPrefix "env" k
      then v
      else abort "Ivalid argument: ${k}, arguments must start with `env`"
    ))
    arguments;
in
makeDerivation (arguments' // {
  builder = path "/makes/utils/make-template/builder.sh";
  inherit name;
  __envArgumentNamesFile = argumentNamesFile;
  __envTemplate = nix.readFile template;
})
