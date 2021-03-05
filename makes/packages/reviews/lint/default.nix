{ makeDerivation
, packages
, path
, nixpkgs
, ...
}:
makeDerivation {
  arguments = {
    envUtilsLintPython = import (path "/makes/utils/lint-python") path nixpkgs;
    envReviewsRuntime = packages.reviews.runtime;
    envSrcReviews = path "/reviews/src/";
  };
  builder = path "/makes/packages/reviews/lint/builder.sh";
  name = "reviews-lint";
}
