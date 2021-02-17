path: pkgs:
let
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
{ envLibraries ? [ ]
, envNodeBinaries ? [ ]
, envNodeLibraries ? [ ]
, envPaths ? [ ]
, envPythonPaths ? [ ]
, envPython37Paths ? [ ]
, envPython38Paths ? [ ]
, envSources ? [ ]
, envUtils ? [ ]
}: makeTemplate {
  arguments = {
    inherit envLibraries;
    inherit envNodeBinaries;
    inherit envNodeLibraries;
    inherit envPaths;
    inherit envPythonPaths;
    inherit envPython37Paths;
    inherit envPython38Paths;
    inherit envSources;
    envUtils = builtins.map (util: import (path util) path pkgs) envUtils;
  };
  name = "makes-utils-make-search-paths";
  template = path "/makes/utils/make-search-paths/template.sh";
}
