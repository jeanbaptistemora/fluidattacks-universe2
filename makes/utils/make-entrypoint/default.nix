# Create an application by replacing arguments in the template

path: pkgs:

{ arguments
, location ? "/bin/${name}"
, name
, searchPaths ? { }
, template
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path pkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path pkgs;
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
      envSearchPaths = makeSearchPaths searchPaths;
      envSearchPathsBase = makeSearchPaths {
        # Minimalistic shell environment
        # Let's try to keep it as lightweight as possible because this
        # propagates to all built apps and packages
        envPaths = [ pkgs.bash pkgs.coreutils ];
      };
      envShell = "${pkgs.bash}/bin/bash";
    };
    name = "utils-make-entrypoint-script-for-${name}";
    template = ''
      #! __envShell__

      unset GEM_PATH
      unset LD_LIBRARY_PATH
      unset NODE_PATH
      unset PATH
      unset PYTHON_PATH

      source __envSearchPathsBase__
      source __envBashLibShopts__
      source __envBashLibCommon__
      source __envSearchPaths__
    '';
  };
  envLocation = location;
  inherit name;
}
