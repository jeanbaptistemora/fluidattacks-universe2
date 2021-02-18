{ integratesPkgs
, packages
, path
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path integratesPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths-deprecated") path integratesPkgs;
in
makeDerivation {
  builder = path "/makes/packages/integrates/front/test/builder.sh";
  envBashLibCommon = path "/makes/utils/common/template.sh";
  envSearchPaths = makeSearchPaths [ integratesPkgs.nodejs ];
  envSetupIntegratesFrontDevRuntime = packages.integrates.front.config.dev-runtime;
  envSrcIntegratesFront = path "/integrates/front";
  name = "integrates-front-test";
}
