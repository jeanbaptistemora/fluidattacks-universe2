{ inputs
, libGit
, makeDerivation
, makeScript
, projectPath
, managePorts
, outputs
, ...
}:
let
  chmodX = name: envSrc: makeDerivation {
    env = { inherit envSrc; };
    builder = "cp $envSrc $out && chmod +x $out";
    inherit name;
  };
  minioCliSrc = inputs.nixpkgs.fetchurl {
    url = "https://dl.min.io/client/mc/release/linux-amd64/archive/mc.RELEASE.2020-09-18T00-13-21Z";
    sha256 = "D9Y4uY4bt131eu2jxVRHdevsFMV5aMUpBkff4LI1M6Q=";
  };
  minioLocalSrc = inputs.nixpkgs.fetchurl {
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
  searchPaths.source = [
    libGit
    (outputs."/utils/aws")
    (outputs."/utils/sops")
    managePorts
  ];
  entrypoint = ./entrypoint.sh;
}
