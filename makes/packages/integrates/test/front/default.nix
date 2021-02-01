{ integratesPkgs
, path
, ...
} @ attrs:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path integratesPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path integratesPkgs;
in
makeDerivation {
  builder = path "/makes/packages/integrates/test/front/builder.sh";
  envBashLibCommon = path "/makes/utils/common/template.sh";
  envSearchPaths = makeSearchPaths [ integratesPkgs.nodejs ];
  envSetupIntegratesDevelopmentFront = import (path "/makes/packages/integrates/config-development/front") attrs.copy;
  envSetupIntegratesRuntimeFront = import (path "/makes/packages/integrates/config-runtime/front") attrs.copy;
  envSrcIntegratesFront = path "/integrates/front";
  name = "integrates-test-front";
}
