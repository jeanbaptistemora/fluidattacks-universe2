{ inputs
, makeScript
, outputs
, ...
}:
let
  mirrorGroup = outputs."/computeOnAwsBatch/observesCodeEtlMirror";
in
makeScript {
  searchPaths = {
    source = [
      (outputs."/utils/aws")
      (inputs.legacy.importUtility "git")
      (inputs.legacy.importUtility "sops")
    ];
  };
  replace = {
    __argCodeEtlMirror__ = "${mirrorGroup}/bin/${mirrorGroup.name}";
  };
  name = "observes-job-code-etl-mirror-all-on-aws";
  entrypoint = ./entrypoint.sh;
}
