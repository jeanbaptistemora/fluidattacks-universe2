pkgs:

rec {
  srcExternalMinIOLocal = pkgs.fetchurl {
    url = "https://dl.min.io/server/minio/release/linux-amd64/archive/minio.RELEASE.2020-09-10T22-02-45Z";
    sha256 = "3a41a1e918a6cb43565aa4ebbb71cfe0a0da1e199a3f727f4a11a4c73a6026b1";
  };
  srcExternalMinIOCli = pkgs.fetchurl {
    url = "https://dl.min.io/client/mc/release/linux-amd64/archive/mc.RELEASE.2020-09-18T00-13-21Z";
    sha256 = "0fd638b98e1bb75df57aeda3c5544775ebec14c57968c5290647dfe0b23533a4";
  };
}
