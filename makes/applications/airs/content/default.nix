{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envAirsContent = path "/airs/content";
    envAirsContentImages = path "/airs/content/images";
    envAirsContentPages = path "/airs/content/pages";
    envAirsImages = path "/airs/theme/2020/static/images";
    envAirsNewFront = path "/airs/new-front";
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
      nixpkgs.utillinux
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
}
