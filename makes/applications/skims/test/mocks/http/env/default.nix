{ makeTemplate
, nixpkgs
, packages
, ...
}:
makeTemplate {
  name = "skims-test-mocks-http-env";
  searchPaths = {
    envPaths = [
      packages.makes.kill-port
      nixpkgs.python38Packages.flask
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.flask
    ];
  };
}
