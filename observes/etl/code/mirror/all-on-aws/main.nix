{
  makeScript,
  outputs,
  ...
}: let
  mirrorGroup = outputs."/computeOnAwsBatch/observesCodeEtlMirror";
in
  makeScript {
    searchPaths = {
      source = [
        outputs."/common/utils/aws"
        outputs."/common/utils/git"
        outputs."/common/utils/sops"
      ];
    };
    replace = {
      __argCodeEtlMirror__ = "${mirrorGroup}/bin/${mirrorGroup.name}";
    };
    name = "observes-etl-code-mirror-all-on-aws";
    entrypoint = ./entrypoint.sh;
  }
