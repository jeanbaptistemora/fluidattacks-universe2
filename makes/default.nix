{ flake
, self
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
      observesPkgs = import srcObservesPkgs { inherit system; };
      observesPkgsTerraform = import srcObservesPkgsTerraform { inherit system; };
      outputs = {
        apps = builtins.mapAttrs makeApp {
          forces-oci-deploy = import (path "/makes/forces/oci-deploy") attrs;
          forces-test = import (path "/makes/forces/test") attrs;
          forces = import (path "/makes/forces/bin") attrs;
          makes-deploy-oci-batch = import (path "/makes/makes/deploy/oci-batch") attrs;
          makes-deploy-oci-ci = import (path "/makes/makes/deploy/oci-ci") attrs;
          makes-lint = import (path "/makes/makes/lint") attrs;
          melts = import (path "/makes/melts/bin") attrs;
          melts-test = import (path "/makes/melts/test") attrs;
          observes-infra-test = import (path "/makes/observes/infra-test") attrs;
          observes-target-redshift = import (path "/makes/observes/bin-target-redshift") attrs;
          observes-tap-json = import (path "/makes/observes/tap-json/bin") attrs;
          skims = import (path "/makes/skims/bin") attrs;
          skims-benchmark = import (path "/makes/skims/benchmark") attrs;
          skims-benchmark-on-aws = import (path "/makes/skims/benchmark-on-aws") attrs;
          skims-docs-deploy = import (path "/makes/skims/docs/deploy") attrs;
          skims-infra-deploy = import (path "/makes/skims/infra-deploy") attrs;
          skims-infra-test = import (path "/makes/skims/infra-test") attrs;
          skims-oci-deploy = import (path "/makes/skims/oci-deploy") attrs;
          skims-process-group = import (path "/makes/skims/process-group") attrs;
          skims-process-group-on-aws = import (path "/makes/skims/process-group-on-aws") attrs;
          skims-process-groups-on-aws = import (path "/makes/skims/process-groups-on-aws") attrs;
          skims-repl = import (path "/makes/skims/bin-repl") attrs;
          skims-test = import (path "/makes/skims/test") attrs;
          sorts = import (path "/makes/sorts/bin") attrs;
          sorts-extract-features = import (path "/makes/sorts/extract-features") attrs;
          sorts-infra-deploy = import (path "/makes/sorts/infra/deploy") attrs;
          sorts-infra-test = import (path "/makes/sorts/infra/test") attrs;
          sorts-test = import (path "/makes/sorts/test") attrs;
          sorts-train-model-on-aws = import (path "/makes/sorts/train") attrs;
        };
        packages = {
          forces-bin = import (path "/makes/forces/bin") attrs;
          forces-lint = import (path "/makes/forces/lint") attrs;
          forces-oci-build = import (path "/makes/forces/oci-build") attrs;
          integrates-lint-front = import (path "/makes/integrates/lint/front") attrs;
          melts-bin = import (path "/makes/melts/bin") attrs;
          melts-lint = import (path "/makes/melts/lint") attrs;
          observes-bin-target-redshift = import (path "/makes/observes/bin-target-redshift") attrs;
          observes-config-python-requirements-target-redshift-runtime = import (path "/makes/observes/config/python-requirements/target-redshift-runtime") attrs;
          observes-config-setup-target-redshift-runtime = (import (path "/makes/observes/config") attrs).setupObservesTargetRedshiftRuntime;
          observes-lint-target-redshift = import (path "/makes/observes/lint-target-redshift") attrs;
          skims-bin = import (path "/makes/skims/bin") attrs;
          skims-bin-repl = import (path "/makes/skims/bin-repl") attrs;
          skims-config-setup-skims-development = (import (path "/makes/skims/config") attrs).setupSkimsDevelopment;
          skims-config-setup-skims-runtime = (import (path "/makes/skims/config") attrs).setupSkimsRuntime;
          skims-config-python-requirements-development = import (path "/makes/skims/config/python-requirements/development") attrs;
          skims-config-python-requirements-runtime = import (path "/makes/skims/config/python-requirements/runtime") attrs;
          skims-docs-build = import (path "/makes/skims/docs/build") attrs;
          skims-lint = import (path "/makes/skims/lint") attrs;
          skims-oci-build = import (path "/makes/skims/oci-build") attrs;
          skims-parsers-antlr = import (path "/makes/skims/parsers/antlr") attrs;
          skims-parsers-babel = import (path "/makes/skims/parsers/babel") attrs;
          skims-security = import (path "/makes/skims/security") attrs;
          skims-structure = import (path "/makes/skims/structure") attrs;
          sorts-bin = import (path "/makes/sorts/bin") attrs;
          sorts-config-python-requirements-development = import (path "/makes/sorts/config/python-requirements/development") attrs;
          sorts-config-python-requirements-runtime = import (path "/makes/sorts/config/python-requirements/runtime") attrs;
          sorts-lint = import (path "/makes/sorts/lint") attrs;
        };
      };
      inherit path;
      makesPkgs = import srcMakesPkgs { inherit system; };
      meltsPkgs = import srcMeltsPkgs { inherit system; };
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
    path = path: /. + (builtins.unsafeDiscardStringContext self.sourceInfo) + path;
  in
  attrs.outputs
)
