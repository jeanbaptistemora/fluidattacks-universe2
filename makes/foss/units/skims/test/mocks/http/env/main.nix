{ inputs
, makeSearchPaths
, outputs
, ...
}:
makeSearchPaths {
  bin = [
    outputs."/makes/kill-port"
    inputs.nixpkgs.python38Packages.flask
  ];
  pythonPackage38 = [
    inputs.nixpkgs.python38Packages.flask
  ];
}
