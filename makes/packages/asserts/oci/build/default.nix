{ applications
, assertsPkgs
, makeOci
, ...
}:
makeOci assertsPkgs {
  config.Entrypoint = [ applications.asserts ];
}
