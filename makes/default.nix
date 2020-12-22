{
  flake,
  pkgsSrcCommon,
  pkgsSrcSkims,
  self,
}:

flake.lib.eachDefaultSystem (
  system:
    let
      attrs = {
        pkgsCommon = import pkgsSrcSkims { inherit system; };
        pkgsSkims = import pkgsSrcSkims { inherit system; };
        self = self;
      };
      makeApp = app: derivation: {
        program = builtins.toString derivation;
        type = "app";
      };
    in
      {
        apps = builtins.mapAttrs makeApp {
          common-deploy-oci = import ../makes/common/deploy/oci attrs;
          skims = import ../makes/skims/bin attrs;
        };
        packages = {
          skims-lint = import ../makes/skims/lint attrs;
          skims-parsers-antlr = import ../makes/skims/parsers/antlr attrs;
          skims-parsers-babel = import ../makes/skims/parsers/babel attrs;
        };
      }
)
