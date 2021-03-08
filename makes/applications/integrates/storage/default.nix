{ fetchurl
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envDevSecrets = path "/integrates/secrets-development.yaml";
    envMinioLocal = fetchurl {
      url = "https://dl.min.io/server/minio/release/linux-amd64/archive/minio.RELEASE.2020-09-10T22-02-45Z";
      sha256 = "OkGh6Rimy0NWWqTru3HP4KDaHhmaP3J/ShGkxzpgJrE=";
    };
    envMinioCli = fetchurl {
      url = "https://dl.min.io/client/mc/release/linux-amd64/archive/mc.RELEASE.2020-09-18T00-13-21Z";
      sha256 = "D9Y4uY4bt131eu2jxVRHdevsFMV5aMUpBkff4LI1M6Q=";
    };
  };
  name = "integrates-storage";
  searchPaths = {
    envPaths = [
      packages.makes.done
      packages.makes.kill-port
      packages.makes.wait
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/storage/entrypoint.sh";
}
