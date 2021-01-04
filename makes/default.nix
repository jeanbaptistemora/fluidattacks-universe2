{
  flake,
  flakeCompat,
  srcCommonPkgs,
  srcMeltsPkgs,
  srcObservesPkgs,
  srcSkimsBenchmarkOwaspRepo,
  srcSkimsPkgs,
  srcSkimsPkgsTerraform,
  self,
}:

flake.lib.eachDefaultSystem (
  system:
    let
      attrs = makeLazyCopy {
        outputs = {
          apps = builtins.mapAttrs makeApp {
            common-deploy-oci-batch = import ../makes/common/deploy/oci-batch attrs;
            common-deploy-oci-ci = import ../makes/common/deploy/oci-ci attrs;
            melts = import ../makes/melts/bin attrs;
            observes-target-redshift = import ../makes/observes/target-redshift/bin attrs;
            observes-tap-json = import ../makes/observes/tap-json/bin attrs;
            skims = import ../makes/skims/bin attrs;
            skims-benchmark = import ../makes/skims/benchmark attrs;
            skims-benchmark-on-aws = import ../makes/skims/benchmark-on-aws attrs;
            skims-docs-deploy = import ../makes/skims/docs/deploy attrs;
            skims-infra-deploy =  import ../makes/skims/infra-deploy attrs;
            skims-infra-test =  import ../makes/skims/infra-test attrs;
            skims-process-group = import ../makes/skims/process-group attrs;
            skims-process-group-on-aws = import ../makes/skims/process-group-on-aws attrs;
            skims-process-groups-on-aws = import ../makes/skims/process-groups-on-aws attrs;
            skims-test =  import ../makes/skims/test attrs;
          };
          packages = {
            melts-bin = import ../makes/melts/bin attrs;
            skims-bin = import ../makes/skims/bin attrs;
            skims-docs-build = import ../makes/skims/docs/build attrs;
            skims-lint = import ../makes/skims/lint attrs;
            skims-parsers-antlr = import ../makes/skims/parsers/antlr attrs;
            skims-parsers-babel = import ../makes/skims/parsers/babel attrs;
            skims-security = import ../makes/skims/security attrs;
            skims-structure = import ../makes/skims/structure attrs;
          };
        };
        commonPkgs = import srcCommonPkgs { inherit system; };
        meltsPkgs = import srcMeltsPkgs { inherit system; };
        observesPkgs = import srcObservesPkgs { inherit system; };
        skimsBenchmarkOwaspRepo = srcSkimsBenchmarkOwaspRepo;
        skimsPkgs = import srcSkimsPkgs { inherit system; };
        skimsPkgsTerraform = import srcSkimsPkgsTerraform { inherit system; };
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
