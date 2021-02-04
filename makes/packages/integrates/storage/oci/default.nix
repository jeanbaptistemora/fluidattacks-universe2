{ integratesPkgs
, outputs
, path
, ...
} @ _:
let
  makeOci = import (path "/makes/utils/make-oci") path integratesPkgs;
in
makeOci {
  config.Entrypoint = [ outputs.apps."integrates/storage".program ];
  config.Env = [
    "SSL_CERT_FILE=${integratesPkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
  ];
  extraCommands = ''
    mkdir tmp
  '';
}
