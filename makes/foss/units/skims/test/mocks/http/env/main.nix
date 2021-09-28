{ inputs
, makeSearchPaths
, ...
}:
makeSearchPaths {
  bin = [
    inputs.product.makes-kill-port
    inputs.nixpkgs.python38Packages.flask
  ];
  pythonPackage38 = [
    inputs.nixpkgs.python38Packages.flask
  ];
}
