{ flake
, srcIntegratesPkgs
, srcMakesPkgs
, srcMeltsPkgs
, srcObservesPkgs
, srcSkimsBenchmarkOwaspRepo
, srcSkimsPkgs
, srcSkimsPkgsTerraform
, srcSkimsTreeSitterRepo
, ...
} @ _:

flake.lib.eachDefaultSystem (
  system:
  let
    attrs = makeLazyCopy {
      outputs = {
        apps = builtins.mapAttrs makeApp {
          makes-deploy-oci-batch = import ../makes/makes/deploy/oci-batch attrs;
          makes-deploy-oci-ci = import ../makes/makes/deploy/oci-ci attrs;
          makes-lint = import ../makes/makes/lint attrs;
          melts = import ../makes/melts/bin attrs;
          observes-target-redshift = import ../makes/observes/target-redshift/bin attrs;
          observes-tap-json = import ../makes/observes/tap-json/bin attrs;
          skims = import ../makes/skims/bin attrs;
          skims-benchmark = import ../makes/skims/benchmark attrs;
          skims-benchmark-on-aws = import ../makes/skims/benchmark-on-aws attrs;
          skims-docs-deploy = import ../makes/skims/docs/deploy attrs;
          skims-infra-deploy = import ../makes/skims/infra-deploy attrs;
          skims-infra-test = import ../makes/skims/infra-test attrs;
          skims-process-group = import ../makes/skims/process-group attrs;
          skims-process-group-on-aws = import ../makes/skims/process-group-on-aws attrs;
          skims-process-groups-on-aws = import ../makes/skims/process-groups-on-aws attrs;
          skims-repl = import ../makes/skims/bin-repl attrs;
          skims-test = import ../makes/skims/test attrs;
        };
        packages = {
          integrates-lint-front = import ../makes/integrates/lint/front attrs;
          melts-bin = import ../makes/melts/bin attrs;
          skims-bin = import ../makes/skims/bin attrs;
          skims-bin-repl = import ../makes/skims/bin-repl attrs;
          skims-config-setup-skims-development = (import ../makes/skims/config attrs).setupSkimsDevelopment;
          skims-config-setup-skims-runtime = (import ../makes/skims/config attrs).setupSkimsRuntime;
          skims-config-python-requirements-development = import ../makes/skims/config/python-requirements/development attrs;
          skims-config-python-requirements-runtime = import ../makes/skims/config/python-requirements/runtime attrs;
          skims-docs-build = import ../makes/skims/docs/build attrs;
          skims-lint = import ../makes/skims/lint attrs;
          skims-parsers-antlr = import ../makes/skims/parsers/antlr attrs;
          skims-parsers-babel = import ../makes/skims/parsers/babel attrs;
          skims-security = import ../makes/skims/security attrs;
          skims-structure = import ../makes/skims/structure attrs;
        };
      };
      integratesPkgs = import srcIntegratesPkgs { inherit system; };
      makesPkgs = import srcMakesPkgs { inherit system; };
      meltsPkgs = import srcMeltsPkgs { inherit system; };
      observesPkgs = import srcObservesPkgs { inherit system; };
      skimsBenchmarkOwaspRepo = srcSkimsBenchmarkOwaspRepo;
      skimsPkgs = import srcSkimsPkgs { inherit system; };
      skimsPkgsTerraform = import srcSkimsPkgsTerraform { inherit system; };
      skimsTreeSitterRepo = srcSkimsTreeSitterRepo;
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
