# Replace arguments in the template

pkgs:

{
  arguments,
  name,
  template,
}:

let
  makeDerivation = import ../../../makes/utils/make-derivation pkgs;

  argumentNames = builtins.attrNames arguments;
  argumentNamesContent = builtins.concatStringsSep "\n" argumentNames;
  argumentNamesFile = builtins.toFile "arguments" "${argumentNamesContent}\n";

  templateFile =
    if (builtins.isString template)
      then builtins.toFile "template" template
      else template;
in
  makeDerivation (arguments // {
    builder = ./builder.sh;
    inherit name;
    __envArgumentNamesFile = argumentNamesFile;
    __envTemplate = templateFile;
  })
