{ makeEntrypoint
, makesPkgs
, packages
, path
, ...
} @ _:
makeEntrypoint makesPkgs {
  searchPaths = {
    envSources = [ packages.reviews.runtime ];
  };
  name = "makes-review-mr";
  template = path "/makes/applications/makes/review-mr/entrypoint.sh";
}
