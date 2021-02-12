# Replace arguments in the template

path: pkgs:

{ arguments ? { }
, argumentsBase64 ? { }
, name
, searchPaths ? { }
, template
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path pkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path pkgs;
  nix = import (path "/makes/utils/nix") path pkgs;

  # Validate arguments
  validateArguments = builtins.mapAttrs
    (k: v: (
      if pkgs.lib.strings.hasPrefix "env" k
      then v
      else abort "Ivalid argument: ${k}, arguments must start with `env`"
    ));

  arguments' = validateArguments arguments;
  argumentsBase64' = validateArguments argumentsBase64;
in
makeDerivation (arguments' // argumentsBase64' // {
  builder = path "/makes/utils/make-template/builder.sh";
  inherit name;
  __envArgumentNamesFile = nix.listToFileWithTrailinNewLine (builtins.attrNames arguments);
  __envArgumentBase64NamesFile = nix.listToFileWithTrailinNewLine (builtins.attrNames argumentsBase64);
  __envTemplate =
    if searchPaths == { }
    then nix.asContent template
    else ''
      source "${makeSearchPaths searchPaths}"

      ${nix.asContent template}
    '';
})
