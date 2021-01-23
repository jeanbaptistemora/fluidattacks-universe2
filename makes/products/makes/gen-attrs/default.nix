{ makesPkgs
, outputs
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path makesPkgs;

  asFile = attrs:
    let
      names = builtins.attrNames attrs;
      namesSorted = builtins.sort (a: b: a < b) names;
      contents = builtins.concatStringsSep "\n" namesSorted;
    in
    builtins.toFile "file" "${contents}\n";
in
makeEntrypoint {
  arguments = {
    envApplications = asFile outputs.apps;
    envPackages = asFile outputs.packages;
  };
  location = "/bin/makes-gen-attrs";
  name = "makes-gen-attrs";
  template = path "/makes/products/makes/gen-attrs/template.sh";
}
