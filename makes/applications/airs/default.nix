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
      airsPkgs.python37
    ];
  };
  template = path "/makes/applications/airs/entrypoint.sh";
}
