{ makeEntrypoint
, reviewsPkgs
, packages
, path
, ...
}:
makeEntrypoint reviewsPkgs {
  searchPaths = {
    envSources = [ packages.reviews.runtime ];
  };
  name = "reviews";
  template = path "/makes/applications/reviews/entrypoint.sh";
}
