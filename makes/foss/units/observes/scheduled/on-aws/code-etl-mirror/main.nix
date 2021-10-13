{ inputs
, makeScript
, outputs
, projectPath
, ...
}:
let
  mirrorGroup = outputs."/computeOnAwsBatch/observesCodeEtlMirror";
in
makeScript {
  searchPaths = {
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "git")
      (inputs.legacy.importUtility "sops")
    ];
  };
  replace = {
    __argCodeEtlMirror__ = "${mirrorGroup}/bin/${mirrorGroup.name}";
  };
  name = "observes-scheduled-on-aws-code-etl-mirror";
  entrypoint = projectPath "/makes/foss/units/observes/scheduled/on-aws/code-etl-mirror/entrypoint.sh";
}
