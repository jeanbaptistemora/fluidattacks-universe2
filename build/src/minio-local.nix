pkgs:

rec {
  srcExternalMinIOLocal = pkgs.fetchurl {
    url = "https://dl.min.io/server/minio/release/linux-amd64/minio";
    sha256 = "9cfaf4bcf56d7f78f3ebd4277fa7fd11f20e59e4e724c468546b7165294b1e96";
  };
  srcExternalMinIOCli = pkgs.fetchurl {
    url = "https://dl.min.io/client/mc/release/linux-amd64/mc";
    sha256 = "7418e5e111c55a3c6f0715b555a952ee47efd8a70fffadf0cd99f66ef1b195f7";
  };
}
