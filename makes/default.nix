{ flake
, srcForcesPkgs
, srcIntegratesPkgs
, srcMakesPkgs
, srcMeltsPkgs
, srcObservesPkgs
, srcObservesPkgsTerraform
, srcSkimsBenchmarkOwaspRepo
, srcSkimsPkgs
, srcSkimsPkgsTerraform
, srcSkimsTreeSitterRepo
, srcSortsPkgs
, ...
} @ _:

flake.lib.eachDefaultSystem (
  system:
  let
    attrs = makeLazyCopy {
      forcesPkgs = import srcForcesPkgs { inherit system; };
      integratesPkgs = import srcIntegratesPkgs { inherit system; };
      outputs = {
        apps = builtins.mapAttrs makeApp {
          forces = import ../makes/forces/bin attrs;
          makes-deploy-oci-batch = import ../makes/makes/deploy/oci-batch attrs;
          makes-deploy-oci-ci = import ../makes/makes/deploy/oci-ci attrs;
          makes-lint = import ../makes/makes/lint attrs;
          melts = import ../makes/melts/bin attrs;
          melts-test = import ../makes/melts/test attrs;
          observes-infra-test = import ../makes/observes/infra-test attrs;
          observes-target-redshift = import ../makes/observes/bin-target-redshift attrs;
          observes-tap-json = import ../makes/observes/tap-json/bin attrs;
          skims = import ../makes/skims/bin attrs;
          skims-benchmark = import ../makes/skims/benchmark attrs;
          skims-benchmark-on-aws = import ../makes/skims/benchmark-on-aws attrs;
          skims-docs-deploy = import ../makes/skims/docs/deploy attrs;
          skims-infra-deploy = import ../makes/skims/infra-deploy attrs;
          skims-infra-test = import ../makes/skims/infra-test attrs;
          skims-oci-deploy = import ../makes/skims/oci-deploy attrs;
          skims-process-group = import ../makes/skims/process-group attrs;
          skims-process-group-on-aws = import ../makes/skims/process-group-on-aws attrs;
          skims-process-groups-on-aws = import ../makes/skims/process-groups-on-aws attrs;
          skims-repl = import ../makes/skims/bin-repl attrs;
          skims-test = import ../makes/skims/test attrs;
          sorts-extract-features = import ../makes/sorts/extract-features attrs;
          sorts-infra-deploy = import ../makes/sorts/infra/deploy attrs;
          sorts-infra-test = import ../makes/sorts/infra/test attrs;
          sorts-test = import ../makes/sorts/test attrs;
        };
        packages = {
          forces-bin = import ../makes/forces/bin attrs;
          forces-lint = import ../makes/forces/lint attrs;
          integrates-lint-front = import ../makes/integrates/lint/front attrs;
          melts-bin = import ../makes/melts/bin attrs;
          melts-lint = import ../makes/melts/lint attrs;
          observes-bin-target-redshift = import ../makes/observes/bin-target-redshift attrs;
          observes-config-python-requirements-target-redshift-runtime = import ../makes/observes/config/python-requirements/target-redshift-runtime attrs;
          observes-config-setup-target-redshift-runtime = (import ../makes/observes/config attrs).setupTargetRedshiftRuntime;
          observes-lint-target-redshift = import ../makes/observes/lint-target-redshift attrs;
          skims-bin = import ../makes/skims/bin attrs;
          skims-bin-repl = import ../makes/skims/bin-repl attrs;
          skims-config-setup-skims-development = (import ../makes/skims/config attrs).setupSkimsDevelopment;
          skims-config-setup-skims-runtime = (import ../makes/skims/config attrs).setupSkimsRuntime;
          skims-config-python-requirements-development = import ../makes/skims/config/python-requirements/development attrs;
          skims-config-python-requirements-runtime = import ../makes/skims/config/python-requirements/runtime attrs;
          skims-docs-build = import ../makes/skims/docs/build attrs;
          skims-lint = import ../makes/skims/lint attrs;
          skims-oci-build = import ../makes/skims/oci-build attrs;
          skims-parsers-antlr = import ../makes/skims/parsers/antlr attrs;
          skims-parsers-babel = import ../makes/skims/parsers/babel attrs;
          skims-security = import ../makes/skims/security attrs;
          skims-structure = import ../makes/skims/structure attrs;
          sorts-config-python-requirements-development = import ../makes/sorts/config/python-requirements/development attrs;
          sorts-config-python-requirements-runtime = import ../makes/sorts/config/python-requirements/runtime attrs;
          sorts-lint = import ../makes/sorts/lint attrs;
        };
      };
      makesPkgs = import srcMakesPkgs { inherit system; };
      meltsPkgs = import srcMeltsPkgs { inherit system; };
      observesPkgs = import srcObservesPkgs { inherit system; };
      observesPkgsTerraform = import srcObservesPkgsTerraform { inherit system; };
      skimsBenchmarkOwaspRepo = srcSkimsBenchmarkOwaspRepo;
      skimsPkgs = import srcSkimsPkgs { inherit system; };
      skimsPkgsTerraform = import srcSkimsPkgsTerraform { inherit system; };
      skimsTreeSitterRepo = srcSkimsTreeSitterRepo;
      sortsPkgs = import srcSortsPkgs { inherit system; };
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
