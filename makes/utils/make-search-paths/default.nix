path: pkgs:
let
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;

  export = envVar: envPath: envDrv:
    "export ${envVar}=\"${envDrv}${envPath}:\${${envVar}:-}\"";

  source = envDrv:
    ''
      if test -e "${envDrv}/template"; then
        source "${envDrv}/template"
      else
        source "${envDrv}"
      fi
    '';
in
{ envClassPaths ? [ ]
, envLibraries ? [ ]
, envMypyPaths ? [ ]
, envMypy38Paths ? [ ]
, envNodeBinaries ? [ ]
, envNodeLibraries ? [ ]
, envPaths ? [ ]
, envPythonPaths ? [ ]
, envPython37Paths ? [ ]
, envPython38Paths ? [ ]
, envPython39Paths ? [ ]
, envSources ? [ ]
, envUtils ? [ ]
}:
makeTemplate {
  name = "makes-utils-make-search-paths";
  template = builtins.concatStringsSep "\n" (builtins.foldl'
    (sources: { generator, derivations }:
      if (derivations == [ ])
      then sources
      else sources ++ (builtins.map generator derivations)
    )
    [ ]
    [
      {
        derivations = envClassPaths;
        generator = export "CLASSPATH" "";
      }
      {
        derivations = envLibraries;
        generator = export "LD_LIBRARY_PATH" "/lib";
      }
      {
        derivations = envLibraries;
        generator = export "LD_LIBRARY_PATH" "/lib64";
      }
      {
        derivations = envMypyPaths;
        generator = export "MYPYPATH" "";
      }
      {
        derivations = envMypy38Paths;
        generator = export "MYPYPATH" "/lib/python3.8/site-packages";
      }
      {
        derivations = envNodeBinaries;
        generator = export "PATH" "/node_modules/.bin";
      }
      {
        derivations = envNodeLibraries;
        generator = export "NODE_PATH" "/node_modules";
      }
      {
        derivations = envPaths;
        generator = export "PATH" "/bin";
      }
      {
        derivations = envPythonPaths;
        generator = export "PYTHONPATH" "";
      }
      {
        derivations = envPython37Paths;
        generator = export "PYTHONPATH" "/lib/python3.7/site-packages";
      }
      {
        derivations = envPython38Paths;
        generator = export "PYTHONPATH" "/lib/python3.8/site-packages";
      }
      {
        derivations = envPython39Paths;
        generator = export "PYTHONPATH" "/lib/python3.9/site-packages";
      }
      {
        derivations = [ (path "/makes/utils/common/template.sh") ];
        generator = source;
      }
      {
        derivations = envSources;
        generator = source;
      }
      {
        derivations = builtins.map (util: import (path util) path pkgs) envUtils;
        generator = source;
      }
    ]);
}
