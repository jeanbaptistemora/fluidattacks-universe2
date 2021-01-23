# Create an application by replacing arguments in the template

path: pkgs:

{ arguments
, location
, name
, template
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path pkgs;
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
makeDerivation {
  builder = path "/makes/utils/make-entrypoint/builder.sh";
  envEntrypoint = makeTemplate {
    inherit arguments;
    inherit name;
    inherit template;
  };
  envEntrypointSetup = makeTemplate {
    arguments = {
      envBashLibCommon = path "/makes/utils/common.sh";
      envBashLibShopts = path "/makes/utils/shopts.sh";
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
  inherit name;
}
