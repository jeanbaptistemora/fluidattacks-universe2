{ integratesPkgs
, outputs
, path
, revision
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path integratesPkgs;
  makeOci = import (path "/makes/utils/make-oci") path integratesPkgs;
in
makeOci {
  config.Env = [
    "CI_COMMIT_SHA=${revision}"
    "SSL_CERT_FILE=${integratesPkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
  ];
  contents = [
    outputs.packages."integrates/back/bin"
    outputs.packages."integrates/back/probes/liveness"
    outputs.packages."integrates/back/probes/readiness"
    (makeDerivation {
      builder = path "/makes/packages/integrates/back/oci/builder.sh";
      envIntegrates = path "/integrates";
      name = "integrates-back-oci-customization";
    })
  ];
}
