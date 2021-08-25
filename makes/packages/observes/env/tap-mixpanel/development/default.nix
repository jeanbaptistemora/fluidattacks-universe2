{ makeTemplate
, nixpkgs
, packages
, ...
}:
let
  pythonPackages = [
    nixpkgs.python38Packages.freezegun
    nixpkgs.python38Packages.iniconfig
    nixpkgs.python38Packages.pluggy
    nixpkgs.python38Packages.py
    nixpkgs.python38Packages.pytest
    nixpkgs.python38Packages.python-dateutil
    nixpkgs.python38Packages.pytest-freezegun
  ];
in
makeTemplate {
  name = "observes-env-tap-mixpanel-development";
  searchPaths = {
    envPaths = pythonPackages;
    envPython38Paths = pythonPackages;
    envSources = [
      packages.observes.env.tap-mixpanel.runtime
    ];
  };
}
