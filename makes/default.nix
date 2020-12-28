{
  flake,
  flakeCompat,
  pkgsSrcCommon,
  pkgsSrcObserves,
  pkgsSrcSkims,
  self,
}:

flake.lib.eachDefaultSystem (
  system:
    let
      attrs = makeLazyCopy {
        outputs = {
          apps = builtins.mapAttrs makeApp {
            common-deploy-oci-ci = import ../makes/common/deploy/oci-ci attrs;
            observes-target-redshift = import ../makes/observes/target-redshift/bin attrs;
            observes-tap-json = import ../makes/observes/tap-json/bin attrs;
            skims = import ../makes/skims/bin attrs;
            skims-benchmark = import ../makes/skims/benchmark attrs;
            skims-benchmark-on-aws = import ../makes/skims/benchmark-on-aws attrs;
            skims-docs-deploy = import ../makes/skims/docs/deploy attrs;
          };
          packages = {
            skims-bin = import ../makes/skims/bin attrs;
            skims-docs-build = import ../makes/skims/docs/build attrs;
            skims-lint = import ../makes/skims/lint attrs;
            skims-parsers-antlr = import ../makes/skims/parsers/antlr attrs;
            skims-parsers-babel = import ../makes/skims/parsers/babel attrs;
            skims-security = import ../makes/skims/security attrs;
            skims-structure = import ../makes/skims/structure attrs;
          };
        };
        pkgsCommon = import pkgsSrcSkims { inherit system; };
        pkgsObserves = import pkgsSrcObserves { inherit system; };
        pkgsSkims = import pkgsSrcSkims { inherit system; };
      };
      makeApp = app: derivation: {
        program = "${derivation}/bin/${app}";
        type = "app";
      };
      makeLazyCopy = attrs: (attrs // {
        copy = makeLazyCopy attrs;
      });
    in
      attrs.outputs
)
