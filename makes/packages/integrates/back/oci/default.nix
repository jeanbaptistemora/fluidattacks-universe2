{ integratesPkgs
, outputs
, path
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path integratesPkgs;
  makeOci = import (path "/makes/utils/make-oci") path integratesPkgs;
in
makeOci {
  config.Entrypoint = [ outputs.apps."integrates/back".program ];
  config.Env = [
    "SSL_CERT_FILE=${integratesPkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
  ];
  contents = [
    (makeDerivation {
      builder = path "/makes/packages/integrates/back/oci/builder.sh";
      envIntegrates = path "/integrates";
      name = "integrates-back-oci-customization";
    })
  ];
}
