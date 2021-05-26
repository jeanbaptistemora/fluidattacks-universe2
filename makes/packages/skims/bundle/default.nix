{ bundleClosure
, packages
, ...
}:
bundleClosure.nix-bootstrap {
  target = packages.skims;
  run = "/bin/skims";
}
