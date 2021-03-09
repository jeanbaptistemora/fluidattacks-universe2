{ makeDerivation
, makeOci
, nixpkgs
, path
, ...
}:
makeOci {
  config = {
    Env = [
      "GIT_SSL_CAINFO=${nixpkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
      "NIX_PATH=/nix/var/nix/profiles/per-user/root/channels"
      "NIX_SSL_CERT_FILE=${nixpkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
      "PATH=/bin:/nix/var/nix/profiles/default/bin"
      "SSL_CERT_FILE=${nixpkgs.cacert}/etc/ssl/certs/ca-bundle.crt"
      "USER=root"
    ];
  };
  contents = [
    (makeDerivation {
      builder = path "/makes/packages/makes/oci/ci/builder.sh";
      name = "makes-oci-ci-customization-layer";
    })
    nixpkgs.bash
    nixpkgs.coreutils
    nixpkgs.git
    nixpkgs.gnutar
    nixpkgs.gzip
    nixpkgs.nix
  ];
}
