{ makes
, nixpkgs
, makeEntrypoint
, packages
, applications
, path
, ...
}:
makeEntrypoint
{
  arguments = {
    envAirsBuild = applications.airs.build;
    envAirsDevelopment = applications.airs.development;
    envSyncGatsby = path "/makes/applications/airs/gatsby.py";
  };
  name = "airs";
  searchPaths = {
    envPaths = [
      nixpkgs.findutils
      nixpkgs.gnused
      nixpkgs.gzip
      nixpkgs.nodejs
      nixpkgs.python38
      nixpkgs.utillinux
      packages.makes.announce.bugsnag
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "gatsby-upload";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  template = path "/makes/applications/airs/entrypoint.sh";
}
