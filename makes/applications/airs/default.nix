{ airsPkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint airsPkgs {
  arguments = {
    envAirsContent = packages.airs.content;
  };
  name = "airs";
  searchPaths = {
    envPaths = [
      airsPkgs.findutils
      airsPkgs.gnused
      airsPkgs.gzip
      airsPkgs.python37
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  template = path "/makes/applications/airs/entrypoint.sh";
}
