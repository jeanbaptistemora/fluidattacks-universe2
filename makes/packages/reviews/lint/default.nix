{ path
, reviewsPkgs
, ...
} @ attrs:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path reviewsPkgs;
in
makeDerivation {
  builder = path "/makes/packages/reviews/lint/builder.sh";
  envUtilsLintPython = import (path "/makes/utils/lint-python") path reviewsPkgs;
  envReviewsRuntime = import (path "/makes/packages/reviews/runtime") attrs.copy;
  envSrcReviews = path "/reviews/src/";
  name = "reviews-lint";
}
