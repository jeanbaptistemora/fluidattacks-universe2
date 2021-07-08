{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envAirsSecrets = path "/airs/deploy/secret-management";
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
      packages.airs.fontawesome
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
}
