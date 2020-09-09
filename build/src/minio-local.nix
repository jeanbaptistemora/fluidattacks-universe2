pkgs:

rec {
  srcExternalMinIOLocal = pkgs.fetchurl {
    url = "https://dl.min.io/server/minio/release/linux-amd64/minio";
    sha256 = "b87a8bddb418a68112f03d32eeda13cb261a5d98ebcf1e468c90e39b9ed13d36";
  };
  srcExternalMinIOCli = pkgs.fetchurl {
    url = "https://dl.min.io/client/mc/release/linux-amd64/mc";
    sha256 = "7418e5e111c55a3c6f0715b555a952ee47efd8a70fffadf0cd99f66ef1b195f7";
  };
}
