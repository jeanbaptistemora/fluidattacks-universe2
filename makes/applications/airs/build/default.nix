{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envAirsNpm = packages.airs.npm;
    envAirsSecrets = path "/airs/secrets";
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
      packages.airs.npm.runtime
      packages.airs.npm.env
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
}
