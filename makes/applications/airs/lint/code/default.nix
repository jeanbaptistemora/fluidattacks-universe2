{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envAirsFront = path "/airs/front";
    envAirsNpm = packages.airs.npm;
    envAirsSecrets = path "/airs/secrets";
  };
  template = path "/makes/applications/airs/lint/code/entrypoint.sh";
  name = "airs-lint-code";
  searchPaths = {
    envPaths = [
      nixpkgs.nodejs
    ];
    envSources = [
      packages.airs.npm.runtime
      packages.airs.npm.env
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/lint-typescript"
      "/makes/utils/sops"
    ];
  };
}
