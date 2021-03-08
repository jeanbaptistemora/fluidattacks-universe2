{ applications
, makeOci
, ...
}:
makeOci {
  config.Entrypoint = [ applications.skims ];
}
