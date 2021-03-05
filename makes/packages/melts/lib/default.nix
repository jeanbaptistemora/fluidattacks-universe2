{ makeTemplate
, packages
, path
, ...
}:
makeTemplate {
  name = "melts-lib";
  searchPaths = {
    envPaths = [ packages.melts ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/git"
    ];
  };
  template = path "/makes/packages/melts/lib/template.sh";
}
