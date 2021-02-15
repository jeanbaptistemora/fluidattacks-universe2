{ integratesPkgs
, applications
, makeEntrypoint
, packages
, path
, ...
} @ _:
makeEntrypoint integratesPkgs {
  arguments = {
    envDevSecrets = path "/integrates/secrets-development.yaml";
    envDone = applications."makes/done";
    envMinioLocal = integratesPkgs.fetchurl {
      url = "https://dl.min.io/server/minio/release/linux-amd64/archive/minio.RELEASE.2020-09-10T22-02-45Z";
      sha256 = "OkGh6Rimy0NWWqTru3HP4KDaHhmaP3J/ShGkxzpgJrE=";
    };
    envMinioCli = integratesPkgs.fetchurl {
      url = "https://dl.min.io/client/mc/release/linux-amd64/archive/mc.RELEASE.2020-09-18T00-13-21Z";
      sha256 = "D9Y4uY4bt131eu2jxVRHdevsFMV5aMUpBkff4LI1M6Q=";
    };
    envUtilsAws = import (path "/makes/utils/aws") path integratesPkgs;
    envUtilsSops = import (path "/makes/utils/sops") path integratesPkgs;
    envWait = applications."makes/wait";
  };
  name = "integrates-storage";
  searchPaths = {
    envPaths = [
      packages."makes/kill-port"
    ];
  };
  template = path "/makes/applications/integrates/storage/entrypoint.sh";
}
