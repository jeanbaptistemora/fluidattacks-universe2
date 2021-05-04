{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envAirsNewFront = path "/airs/new-front";
    envAirsNpm = packages.airs.npm;
    envAirsSecrets = path "/airs/deploy/secret-management";
  };
  template = path "/makes/applications/airs/lint/code/entrypoint.sh";
  name = "airs-lint-code";
  searchPaths = {
    envPaths = [
      nixpkgs.nodejs
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/lint-typescript"
      "/makes/utils/sops"
    ];
  };
}
