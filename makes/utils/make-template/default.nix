# Replace arguments in the template

path: pkgs:

{ arguments
, name
, template
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path pkgs;

  argumentNames = builtins.attrNames arguments;
  argumentNamesContent = builtins.concatStringsSep "\n" argumentNames;
  argumentNamesFile = builtins.toFile "arguments" "${argumentNamesContent}\n";

  templateFile =
    if (builtins.isString template)
    then builtins.toFile "template" template
    else template;
in
makeDerivation (arguments // {
  builder = path "/makes/utils/make-template/builder.sh";
  inherit name;
  __envArgumentNamesFile = argumentNamesFile;
  __envTemplate = templateFile;
})
