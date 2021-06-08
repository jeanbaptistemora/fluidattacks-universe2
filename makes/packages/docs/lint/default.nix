{ makeDerivation
, path
, ...
}:
makeDerivation {
  arguments = {
    envSrcDocsDevelopment = path "/docs/src/docs/development/";
    envSrcDocsAbout = path "/docs/src/docs/about/";
  };
  builder = path "/makes/packages/docs/lint/builder.sh";
  name = "docs-lint";
  searchPaths = {
    envUtils = [ "/makes/utils/lint-markdown" ];
  };
}
