{ makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  self = path "/observes/singer/tap_mixpanel";
in
makeTemplate {
  name = "observes-env-tap-mixpanel-runtime";
  searchPaths = {
    envLibraries = [
      nixpkgs.gcc.cc.lib
    ];
    envMypyPaths = [
      self
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.boto3
      nixpkgs.python38Packages.botocore
      nixpkgs.python38Packages.chardet
      nixpkgs.python38Packages.certifi
      nixpkgs.python38Packages.idna
      nixpkgs.python38Packages.numpy
      nixpkgs.python38Packages.pandas
      nixpkgs.python38Packages.ratelimiter
      nixpkgs.python38Packages.requests
      nixpkgs.python38Packages.urllib3
    ];
    envSources = [
      packages.observes.env.singer-io.runtime
    ];
  };
}
