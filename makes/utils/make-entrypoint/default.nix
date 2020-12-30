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
      arguments = arguments;
      name = name;
      template = template;
    };
    envEntrypointSetup = makeTemplate {
      arguments = {
        envBashLibCommon = ../../../makes/utils/bash-lib/common.sh;
        envBashLibShopts = ../../../makes/utils/bash-lib/shopts.sh;
        envShell = "${pkgs.bash}/bin/bash";
      };
      name = "utils-make-entrypoint-script";
      template = ''
        #! __envShell__

        source __envBashLibShopts__
        source __envBashLibCommon__
      '';
    };
    envLocation = location;
    name = name;
  }
