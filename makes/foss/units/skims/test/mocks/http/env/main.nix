{ inputs
, makeSearchPaths
, managePorts
, ...
}:
makeSearchPaths {
  bin = [
    inputs.nixpkgs.python38Packages.flask
  ];
  source = [
    managePorts
  ];
  pythonPackage38 = [
    inputs.nixpkgs.python38Packages.flask
  ];
}
