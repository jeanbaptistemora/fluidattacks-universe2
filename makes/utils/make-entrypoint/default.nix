# Create an application by replacing arguments in the template

path: pkgs:

{ arguments
, location ? "/bin/${name}"
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
      envBashLibCommon = path "/makes/utils/common/template.sh";
      envBashLibShopts = path "/makes/utils/shopts/template.sh";
      envPath = pkgs.lib.strings.makeBinPath [
        # Minimalistic shell environment
        # Let's try to keep it as lightweight as possible because this
        # propagates to all built apps and packages
        pkgs.bash
        pkgs.coreutils
      ];
      envShell = "${pkgs.bash}/bin/bash";
    };
    name = "utils-make-entrypoint-script";
    template = ''
      #! __envShell__

      export PATH='__envPath__'

      source __envBashLibShopts__
      source __envBashLibCommon__

      unset LD_LIBRARY_PATH
    '';
  };
  envLocation = location;
  inherit name;
}
