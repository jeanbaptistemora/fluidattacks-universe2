{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envAirsNpm = packages.airs.npm;
    envAirsSecrets = path "/airs/deploy/secret-management";
  };
  template = path "/makes/applications/airs/build/entrypoint.sh";
  name = "airs-build";
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
