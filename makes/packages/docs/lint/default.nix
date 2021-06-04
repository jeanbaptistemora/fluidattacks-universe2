{ makeDerivation
, path
, ...
}:
makeDerivation {
  arguments = {
    envSrcDocs = path "/docs/src/docs";
  };
  builder = path "/makes/packages/docs/lint/builder.sh";
  name = "docs-lint";
  searchPaths = {
    envUtils = [ "/makes/utils/lint-markdown" ];
  };
}
