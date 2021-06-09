{ makeDerivation
, path
, ...
}:
makeDerivation {
  arguments = {
    envSrcDocsDevelopment = path "/docs/src/docs/development/";
    envSrcDocsAbout = path "/docs/src/docs/about/";
    envSrcDocsSquad = path "/docs/src/docs/squad/";
    envSrcDocsMachine = path "/docs/src/docs/machine/";
  };
  builder = path "/makes/packages/docs/lint/builder.sh";
  name = "docs-lint";
  searchPaths = {
    envUtils = [ "/makes/utils/lint-markdown" ];
  };
}
