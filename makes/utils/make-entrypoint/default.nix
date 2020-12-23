# Create an application by replacing arguments in the template

pkgs:

{
  arguments,
  location,
  name,
  template,
}:

let
  makeDerivation = import ../../../makes/utils/make-derivation pkgs;
  makeTemplate = import ../../../makes/utils/make-template pkgs;
in
  makeDerivation {
    builder = ./builder.sh;
    envEntrypoint = makeTemplate {
      arguments = (arguments // {
        makeEntrypoint = makeTemplate {
          arguments = {
            envBashLibCommon = ../../../makes/utils/bash-lib/common.sh;
            envBashLibShopts = ../../../makes/utils/bash-lib/shopts.sh;
          };
          name = "utils-make-entrypoint-script";
          template = ''
            source '__envBashLibShopts__'
            source '__envBashLibCommon__'
          '';
        };
      });
      executable = true;
      name = name;
      template = template;
    };
    envLocation = location;
    name = name;
  }
