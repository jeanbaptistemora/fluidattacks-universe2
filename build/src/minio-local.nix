pkgs:

rec {
  srcExternalMinIOLocal = pkgs.fetchurl {
    url = "https://dl.min.io/server/minio/release/linux-amd64/minio";
    sha256 = "9cfaf4bcf56d7f78f3ebd4277fa7fd11f20e59e4e724c468546b7165294b1e96";
  };
}
