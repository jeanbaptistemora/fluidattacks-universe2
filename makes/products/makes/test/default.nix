{ makesPkgs
, path
, sources
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path makesPkgs;
in
makeEntrypoint {
  arguments = {
    envBuilt = builtins.concatLists [
      (builtins.attrValues (builtins.removeAttrs sources.apps [
        "makes-test" # Needed to avoid infinite recursion
        "skims-oci-deploy" # Consumes a lot of disk
      ]))
      (builtins.attrValues (builtins.removeAttrs sources.packages [
        "skims-oci-build" # Consumes a lot of disk
      ]))
    ];
  };
  location = "/bin/makes-test";
  name = "makes-test";
  template = path "/makes/products/makes/test/entrypoint.sh";
}
