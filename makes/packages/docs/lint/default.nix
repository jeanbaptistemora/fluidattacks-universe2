{ makeDerivation
, path
, ...
}:
makeDerivation {
  arguments = {
    envSrcDocsDevelopment = path "/docs/src/docs/development/";
  };
  builder = path "/makes/packages/docs/lint/builder.sh";
  name = "docs-lint";
  searchPaths = {
    envUtils = [ "/makes/utils/lint-markdown" ];
  };
}
