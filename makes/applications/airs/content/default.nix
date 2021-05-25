{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envAirsContent = path "/airs/content";
    envAirsNpm = packages.airs.npm;
    envAirsSecrets = path "/airs/deploy/secret-management";
  };
  template = path "/makes/applications/airs/content/entrypoint.sh";
  name = "airs-content";
  searchPaths = {
    envLibraries = [
      nixpkgs.musl
    ];
    envPaths = [
      nixpkgs.findutils
      nixpkgs.gnugrep
      nixpkgs.gnused
      nixpkgs.nodejs
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
