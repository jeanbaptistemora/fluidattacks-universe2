# Create an application by replacing arguments in the template

pkgs:

{
  arguments,
  name,
  template,
}:

let
  make = import ../../../makes/utils/make pkgs;
  makeTemplate = import ../../../makes/utils/make-template pkgs;
in
  make {
    builder = ./builder.sh;
    envEntrypoint = makeTemplate {
      arguments = arguments;
      executable = true;
      name = name;
      template = template;
    };
    name = "utils-make-app-${name}";
  }
