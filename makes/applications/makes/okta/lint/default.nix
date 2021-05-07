{ makeEntrypoint
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envSrcMakesOktaParser = path "/makes/applications/makes/okta/src/terraform/parser";
  };
  name = "makes-okta-lint";
  searchPaths = {
    envUtils = [
      "/makes/utils/lint-python"
    ];
  };
  template = path "/makes/applications/makes/okta/lint/entrypoint.sh";
}
