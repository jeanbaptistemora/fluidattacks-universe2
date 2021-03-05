{ applications
, makeOci
, ...
}:
makeOci {
  config.Entrypoint = [ applications.asserts ];
}
