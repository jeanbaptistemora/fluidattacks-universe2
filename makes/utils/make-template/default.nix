# Replace arguments in the template

pkgs:

{
  arguments,
  executable ? false,
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
    name = name;
    __envArgumentNamesFile = argumentNamesFile;
    __envExecutable = executable;
    __envTemplate = templateFile;
  })
