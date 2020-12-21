# Replace arguments in the template

pkgs:

{
  arguments,
  executable ? false,
  name,
  template,
}:

let
  make = import ../../../makes/utils/make pkgs;

  argumentNames = builtins.attrNames arguments;
  argumentNamesContent = builtins.concatStringsSep "\n" argumentNames;
  argumentNamesFile = builtins.toFile "arguments" "${argumentNamesContent}\n";
in
  make (arguments // {
    builder = ./builder.sh;
    name = "utils-make-template-${name}";
    __envArgumentNamesFile = argumentNamesFile;
    __envExecutable = executable;
    __envTemplate = template;
  })
