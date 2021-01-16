{ outputs
, skimsPkgs
, ...
} @ _:
let
  makeOci = import ../../../makes/utils/make-oci skimsPkgs;
in
makeOci {
  config.Entrypoint = "skims";
  contents = [ outputs.packages.skims-bin ];
  name = "skims-oci-build";
}
