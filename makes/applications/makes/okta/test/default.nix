{ makeEntrypoint
, nixpkgs
, path
, terraformTest
, ...
}:
makeEntrypoint {
  name = "makes-okta-test";
  arguments = {
    envData = path "/makes/applications/makes/okta/src/terraform/data.yaml";
    envParser = path "/makes/applications/makes/okta/src/terraform/parser/__init__.py";
    envPermissions = "dev";
    envProduct = "makes";
  };
  searchPaths = {
    envPaths = [
      nixpkgs.python38
      (terraformTest {
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
