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
  argumentsContent = builtins.concatStringsSep "\n" argumentNames;
  arguments = builtins.toFile "arguments" argumentsContent;
in
  make {
    builder = ./builder.sh;
    name = "utils-make-template-${name}";
    __envArguments = arguments;
    __envExecutable = executable;
    __envTemplate = template;
  }
