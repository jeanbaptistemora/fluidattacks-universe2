{ makeTemplate
, meltsPkgs
, packages
, path
, ...
} @ _:
makeTemplate meltsPkgs {
  name = "melts-lib";
  searchPaths = {
    envPaths = [ packages.melts ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/use-git-repo"
    ];
  };
  template = path "/makes/packages/melts/lib/template.sh";
}
