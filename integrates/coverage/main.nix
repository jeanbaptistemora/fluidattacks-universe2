{
  inputs,
  makeDerivation,
  makePythonPypiEnvironment,
  makeScript,
  projectPath,
  outputs,
  ...
}: let
  chmodX = name: envSrc:
    makeDerivation {
      env = {inherit envSrc;};
      builder = "cp $envSrc $out && chmod +x $out";
      inherit name;
    };
  codecovSrc = inputs.nixpkgs.fetchurl {
    url = "https://uploader.codecov.io/v0.2.1/linux/codecov";
    sha256 = "14kff14mk11kkf7jisr4c8r9bvdyx212drgb2v435blhafrxnpwb";
  };
in
  makeScript {
    replace = {
      __argSecretsDev__ = projectPath "/integrates/secrets/development.yaml";
      __argCodecov__ = chmodX "codecov" codecovSrc;
    };
    name = "integrates-coverage";
    searchPaths = {
      bin = [
        inputs.nixpkgs.findutils
        inputs.nixpkgs.git
      ];
      source = [
        (makePythonPypiEnvironment {
          name = "integrates-coverage";
          sourcesYaml = ./pypi-sources.yaml;
        })
        outputs."/common/utils/sops"
      ];
    };
    entrypoint = ./entrypoint.sh;
  }
