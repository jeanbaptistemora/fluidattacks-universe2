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
in
  makeDerivation (arguments // {
    builder = ./builder.sh;
    name = "utils-make-template-${name}";
    __envArgumentNamesFile = argumentNamesFile;
    __envExecutable = executable;
    __envTemplate = template;
  })
