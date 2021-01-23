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

flake.lib.eachSystem [ "x86_64-linux" ] (
  system:
  let
    attrs = makeLazyCopy {
      forcesPkgs = import srcForcesPkgs { inherit system; };
      integratesPkgs = import srcIntegratesPkgs { inherit system; };
      observesPkgs = import srcObservesPkgs { inherit system; };
      observesPkgsTerraform = import srcObservesPkgsTerraform { inherit system; };
      outputs = {
        apps = builtins.mapAttrs makeApp {
          forces-oci-deploy = import (path "/makes/products/forces/oci-deploy") attrs;
          forces-test = import (path "/makes/products/forces/test") attrs;
          forces = import (path "/makes/products/forces/bin") attrs;
          makes-deploy-oci-batch = import (path "/makes/products/makes/deploy/oci-batch") attrs;
          makes-deploy-oci-ci = import (path "/makes/products/makes/deploy/oci-ci") attrs;
          makes-lint = import (path "/makes/products/makes/lint") attrs;
          melts = import (path "/makes/products/melts/bin") attrs;
          melts-test = import (path "/makes/products/melts/test") attrs;
          observes-infra-test = import (path "/makes/products/observes/infra-test") attrs;
          observes-target-redshift = import (path "/makes/products/observes/bin-target-redshift") attrs;
          observes-tap-json = import (path "/makes/products/observes/tap-json/bin") attrs;
          skims = import (path "/makes/products/skims/bin") attrs;
          skims-benchmark = import (path "/makes/products/skims/benchmark") attrs;
          skims-benchmark-on-aws = import (path "/makes/products/skims/benchmark-on-aws") attrs;
          skims-docs-deploy = import (path "/makes/products/skims/docs/deploy") attrs;
          skims-infra-deploy = import (path "/makes/products/skims/infra-deploy") attrs;
          skims-infra-test = import (path "/makes/products/skims/infra-test") attrs;
          skims-oci-deploy = import (path "/makes/products/skims/oci-deploy") attrs;
          skims-process-group = import (path "/makes/products/skims/process-group") attrs;
          skims-process-group-on-aws = import (path "/makes/products/skims/process-group-on-aws") attrs;
          skims-process-groups-on-aws = import (path "/makes/products/skims/process-groups-on-aws") attrs;
          skims-repl = import (path "/makes/products/skims/bin-repl") attrs;
          skims-test = import (path "/makes/products/skims/test") attrs;
          sorts = import (path "/makes/products/sorts/bin") attrs;
          sorts-extract-features = import (path "/makes/products/sorts/extract-features") attrs;
          sorts-infra-deploy = import (path "/makes/products/sorts/infra/deploy") attrs;
          sorts-infra-test = import (path "/makes/products/sorts/infra/test") attrs;
          sorts-test = import (path "/makes/products/sorts/test") attrs;
          sorts-train-model-on-aws = import (path "/makes/products/sorts/train") attrs;
        };
        packages = {
          forces-bin = import (path "/makes/products/forces/bin") attrs;
          forces-lint = import (path "/makes/products/forces/lint") attrs;
          forces-oci-build = import (path "/makes/products/forces/oci-build") attrs;
          integrates-lint-front = import (path "/makes/products/integrates/lint/front") attrs;
          makes-dev = import (path "/makes/products/makes/dev") attrs;
          melts-bin = import (path "/makes/products/melts/bin") attrs;
          melts-lint = import (path "/makes/products/melts/lint") attrs;
          observes-bin-target-redshift = import (path "/makes/products/observes/bin-target-redshift") attrs;
          observes-config-python-requirements-target-redshift-runtime = import (path "/makes/products/observes/config/python-requirements/target-redshift-runtime") attrs;
          observes-config-setup-target-redshift-runtime = (import (path "/makes/products/observes/config") attrs).setupObservesTargetRedshiftRuntime;
          observes-lint-target-redshift = import (path "/makes/products/observes/lint-target-redshift") attrs;
          skims-bin = import (path "/makes/products/skims/bin") attrs;
          skims-bin-repl = import (path "/makes/products/skims/bin-repl") attrs;
          skims-config-setup-skims-development = (import (path "/makes/products/skims/config") attrs).setupSkimsDevelopment;
          skims-config-setup-skims-runtime = (import (path "/makes/products/skims/config") attrs).setupSkimsRuntime;
          skims-config-python-requirements-development = import (path "/makes/products/skims/config/python-requirements/development") attrs;
          skims-config-python-requirements-runtime = import (path "/makes/products/skims/config/python-requirements/runtime") attrs;
          skims-docs-build = import (path "/makes/products/skims/docs/build") attrs;
          skims-lint = import (path "/makes/products/skims/lint") attrs;
          skims-oci-build = import (path "/makes/products/skims/oci-build") attrs;
          skims-parsers-antlr = import (path "/makes/products/skims/parsers/antlr") attrs;
          skims-parsers-babel = import (path "/makes/products/skims/parsers/babel") attrs;
          skims-security = import (path "/makes/products/skims/security") attrs;
          skims-structure = import (path "/makes/products/skims/structure") attrs;
          sorts-bin = import (path "/makes/products/sorts/bin") attrs;
          sorts-config-python-requirements-development = import (path "/makes/products/sorts/config/python-requirements/development") attrs;
          sorts-config-python-requirements-runtime = import (path "/makes/products/sorts/config/python-requirements/runtime") attrs;
          sorts-lint = import (path "/makes/products/sorts/lint") attrs;
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
