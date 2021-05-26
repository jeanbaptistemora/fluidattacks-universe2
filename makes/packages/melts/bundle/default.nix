{ bundleClosure
, packages
, ...
}:
bundleClosure.nix-bootstrap {
  target = packages.melts;
  run = "/bin/melts";
}
