pkgs:

rec {
  srcExternalMinIOLocal = pkgs.fetchurl {
    url = "https://dl.min.io/server/minio/release/linux-amd64/archive/minio.RELEASE.2020-09-10T22-02-45Z";
    sha256 = "3a41a1e918a6cb43565aa4ebbb71cfe0a0da1e199a3f727f4a11a4c73a6026b1";
  };
  srcExternalMinIOCli = pkgs.fetchurl {
    url = "https://dl.min.io/client/mc/release/linux-amd64/mc.RELEASE.2020-09-03T00-08-28Z";
    sha256 = "7418e5e111c55a3c6f0715b555a952ee47efd8a70fffadf0cd99f66ef1b195f7";
  };
}
