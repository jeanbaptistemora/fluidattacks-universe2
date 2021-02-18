{ makeEntrypoint
, reviewsPkgs
, packages
, path
, ...
} @ _:
makeEntrypoint reviewsPkgs {
  searchPaths = {
    envSources = [ packages.reviews.runtime ];
  };
  name = "makes-reviews";
  template = path "/makes/applications/reviews/entrypoint.sh";
}
