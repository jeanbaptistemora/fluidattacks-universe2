{ makeTemplate
, nixpkgs
, path
, ...
}:
makeTemplate {
  name = "observes-generic-linter";
  searchPaths = {
    envPaths = [
      nixpkgs.findutils
    ];
    envUtils = [
      "/makes/utils/lint-python"
    ];
  };
  template = path "/makes/packages/observes/generic/linter/builder.sh";
}
