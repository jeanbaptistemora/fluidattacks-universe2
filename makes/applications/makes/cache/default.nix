{ applications
, makesPkgs
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path makesPkgs;
in
makeEntrypoint {
  arguments = {
    envKillPidListeningOnPort = import (path "/makes/utils/kill-pid-listening-on-port") path makesPkgs;
    envMinioCli = makesPkgs.fetchurl {
      url = "https://dl.min.io/client/mc/release/linux-amd64/archive/mc.RELEASE.2020-09-18T00-13-21Z";
      sha256 = "D9Y4uY4bt131eu2jxVRHdevsFMV5aMUpBkff4LI1M6Q=";
    };
    envMinioLocal = makesPkgs.fetchurl {
      url = "https://dl.min.io/server/minio/release/linux-amd64/archive/minio.RELEASE.2020-09-10T22-02-45Z";
      sha256 = "OkGh6Rimy0NWWqTru3HP4KDaHhmaP3J/ShGkxzpgJrE=";
    };
    envWait = applications."makes/wait";
  };
  name = "makes-cache";
  template = path "/makes/applications/makes/cache/entrypoint.sh";
}
