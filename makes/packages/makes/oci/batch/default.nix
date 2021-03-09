{ makeDerivation
, makeOci
, nixpkgs
, path
, ...
}:
makeOci {
  config = {
    Env = [
      "GIT_SSL_CAINFO=/etc/ssl/certs/ca-bundle.crt"
      "NIX_PATH=/nix/var/nix/profiles/per-user/root/channels"
      "NIX_SSL_CERT_FILE=/etc/ssl/certs/ca-bundle.crt"
      "PATH=/bin:/nix/var/nix/profiles/default/bin"
      "SSL_CERT_FILE=/etc/ssl/certs/ca-bundle.crt"
      "SYSTEM_CERTIFICATE_PATH=/etc/ssl/certs/ca-bundle.crt"
      "USER=root"
    ];
    WorkingDir = "/product";
  };
  contents = [
    (makeDerivation {
      arguments = {
        envRoot = path "/";
      };
      builder = path "/makes/packages/makes/oci/batch/builder.sh";
      name = "makes-oci-batch-customization-layer";
    })
    nixpkgs.bash
    nixpkgs.cacert
    nixpkgs.coreutils
    nixpkgs.git
    nixpkgs.gnutar
    nixpkgs.gzip
    nixpkgs.nix
  ];
}
