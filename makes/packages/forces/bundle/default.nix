{ bundleClosure
, packages
, ...
}:
bundleClosure.nix-bootstrap {
  target = packages.forces;
  run = "/bin/forces";
}
