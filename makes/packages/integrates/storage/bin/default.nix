{ integratesPkgs
, outputs
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
in
makeEntrypoint {
  arguments = {
    envMinioLocal = integratesPkgs.fetchurl {
      url = "https://dl.min.io/server/minio/release/linux-amd64/archive/minio.RELEASE.2020-09-10T22-02-45Z";
      sha256 = "OkGh6Rimy0NWWqTru3HP4KDaHhmaP3J/ShGkxzpgJrE=";
    };
    envMinioCli = integratesPkgs.fetchurl {
      url = "https://dl.min.io/client/mc/release/linux-amd64/archive/mc.RELEASE.2020-09-18T00-13-21Z";
      sha256 = "D9Y4uY4bt131eu2jxVRHdevsFMV5aMUpBkff4LI1M6Q=";
    };
    envKillPidListeningOnPort = import (path "/makes/utils/kill-pid-listening-on-port") path integratesPkgs;
    envUtilsAws = import (path "/makes/utils/aws") path integratesPkgs;
    envUtilsSops = import (path "/makes/utils/sops") path integratesPkgs;
    envWait = outputs.apps."makes/wait".program;
  };
  name = "integrates-storage";
  template = path "/makes/packages/integrates/storage/bin/entrypoint.sh";
}
