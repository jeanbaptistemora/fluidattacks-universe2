{ makeDerivation
, path
, ...
}:
makeDerivation {
  arguments = {
    envSrcDocs = path "/docs/src/docs/development/stack";
  };
  builder = path "/makes/packages/docs/lint/builder.sh";
  name = "docs-lint";
  searchPaths = {
    envUtils = [ "/makes/utils/lint-markdown" ];
  };
}
