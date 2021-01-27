path: pkgs:
let
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
derivations: makeTemplate {
  arguments = {
    envBinPath = pkgs.lib.strings.makeBinPath derivations;
    envLibPath = pkgs.lib.strings.makeLibraryPath derivations;
    envNodePath = pkgs.lib.strings.makeSearchPath "node_modules" derivations;
    envPyPath = builtins.concatStringsSep ":" [
      (pkgs.lib.strings.makeSearchPath "lib/python3.8/site-packages" derivations)
      (pkgs.lib.strings.makeSearchPath "lib/python3.7/site-packages" derivations)
    ];
  };
  name = "makes-utils-make-search-paths";
  template = path "/makes/utils/make-search-paths/setup-paths-template.sh";
}
