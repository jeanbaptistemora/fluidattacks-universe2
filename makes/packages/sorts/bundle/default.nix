{ bundleClosure
, packages
, ...
}:
bundleClosure.nix-bootstrap {
  target = packages.sorts;
  run = "/bin/sorts";
}
