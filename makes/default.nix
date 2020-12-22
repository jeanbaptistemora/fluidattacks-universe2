{
  flake,
  pkgsSrcCommon,
  pkgsSrcSkims,
  self,
}:

flake.lib.eachDefaultSystem (
  system:
    let
      attrs = makeLazyCopy {
        outputs = {
          apps = builtins.mapAttrs makeApp {
            common-deploy-oci = import ../makes/common/deploy/oci attrs;
            skims = import ../makes/skims/bin attrs;
          };
          packages = {
            skims-docs-build = import ../makes/skims/docs/build attrs;
            skims-lint = import ../makes/skims/lint attrs;
            skims-parsers-antlr = import ../makes/skims/parsers/antlr attrs;
            skims-parsers-babel = import ../makes/skims/parsers/babel attrs;
            skims-security = import ../makes/skims/security attrs;
          };
        };
        pkgsCommon = import pkgsSrcSkims { inherit system; };
        pkgsSkims = import pkgsSrcSkims { inherit system; };
      };
      makeApp = app: derivation: {
        program = builtins.toString derivation;
        type = "app";
      };
      makeLazyCopy = attrs: (attrs // {
        copy = makeLazyCopy attrs;
      });
    in
      attrs.outputs
)
