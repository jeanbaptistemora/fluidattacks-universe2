{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envAirsSecrets = path "/airs/secrets";
  };
  template = path "/makes/applications/airs/development/entrypoint.sh";
  name = "airs-development";
  searchPaths = {
    envLibraries = [
      nixpkgs.musl
    ];
    envPaths = [
      nixpkgs.utillinux
    ];
    envSources = [
      packages.airs.npm.runtime
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
}
