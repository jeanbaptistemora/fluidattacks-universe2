{ entrypoint
, name
, nixPkgs
, path
, packageEnv
, python
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixPkgs;
in
makeEntrypoint {
  inherit name;
  arguments = {
    envPython = "${python}/bin/python";
    envPackage = packageEnv;
    envEntrypoint = entrypoint;
  };
  template = path "/makes/libs/observes/build-bin/entrypoint.sh";
}
