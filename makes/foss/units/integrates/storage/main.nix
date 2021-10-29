{ fetchUrl
, libGit
, makeDerivation
, makeScript
, inputs
, outputs
, projectPath
, ...
}:
let
  chmodX = name: envSrc: makeDerivation {
    env = { inherit envSrc; };
    builder = "cp $envSrc $out && chmod +x $out";
    inherit name;
  };
  minioCliSrc = fetchUrl {
    url = "https://dl.min.io/client/mc/release/linux-amd64/archive/mc.RELEASE.2020-09-18T00-13-21Z";
    sha256 = "D9Y4uY4bt131eu2jxVRHdevsFMV5aMUpBkff4LI1M6Q=";
  };
  minioLocalSrc = fetchUrl {
    url = "https://dl.min.io/server/minio/release/linux-amd64/archive/minio.RELEASE.2020-09-10T22-02-45Z";
    sha256 = "OkGh6Rimy0NWWqTru3HP4KDaHhmaP3J/ShGkxzpgJrE=";
  };
in
makeScript {
  replace = {
    __argDevSecrets__ = projectPath "/integrates/secrets-development.yaml";
    __argMinioCli__ = chmodX "minio-cli" minioCliSrc;
    __argMinioLocal__ = chmodX "minio-local" minioLocalSrc;
  };
  name = "integrates-storage";
  searchPaths = {
    bin = [
      outputs."/makes/done"
      outputs."/makes/kill-port"
      outputs."/makes/wait"
    ];
    source = [
      libGit
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  entrypoint = projectPath "/makes/foss/units/integrates/storage/entrypoint.sh";
}
