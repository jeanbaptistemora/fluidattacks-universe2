{ integratesPkgs
, outputs
, path
, ...
} @ _:
let
  makeOci = import (path "/makes/utils/make-oci") path integratesPkgs;
in
makeOci {
  config.Entrypoint = [ outputs.apps."integrates/dynamo".program ];
  contents = [
    integratesPkgs.cacert
  ];
  extraCommands = ''
    mkdir tmp
  '';
}
