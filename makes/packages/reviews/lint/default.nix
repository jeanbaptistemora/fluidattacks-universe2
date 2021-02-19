{ makeDerivation
, packages
, path
, reviewsPkgs
, ...
} @ _:
makeDerivation reviewsPkgs {
  arguments = {
    envUtilsLintPython = import (path "/makes/utils/lint-python") path reviewsPkgs;
    envReviewsRuntime = packages.reviews.runtime;
    envSrcReviews = path "/reviews/src/";
  };
  builder = path "/makes/packages/reviews/lint/builder.sh";
  name = "reviews-lint";
}
