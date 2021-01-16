{ outputs
, skimsPkgs
, ...
} @ _:
let
  makeOci = import ../../../makes/utils/make-oci skimsPkgs;
in
makeOci {
  config.Entrypoint = [ outputs.apps.skims.program ];
}
