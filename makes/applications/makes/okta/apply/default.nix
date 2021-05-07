{ makeEntrypoint
, nixpkgs
, path
, terraformApply
, ...
}:
makeEntrypoint {
  name = "makes-okta-apply";
  arguments = {
    envData = path "/makes/applications/makes/okta/src/terraform/data.yaml";
    envParser = path "/makes/applications/makes/okta/src/terraform/parser/__init__.py";
    envPermissions = "prod";
    envProduct = "makes";
  };
  searchPaths = {
    envPaths = [
      nixpkgs.python38
      (terraformApply {
        name = "terraform";
        product = "makes";
        target = "makes/applications/makes/okta/src/terraform";
        secretsPath = "makes/applications/makes/okta/src/terraform/data.yaml";
      })
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/makes/okta/entrypoint.sh";
}
