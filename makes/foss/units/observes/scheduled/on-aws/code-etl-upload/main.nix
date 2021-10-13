{ inputs
, outputs
, makeScript
, projectPath
, ...
}:
let
  uploadGroup = outputs."/computeOnAwsBatch/observesCodeEtlUpload";
in
makeScript {
  searchPaths = {
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "git")
      (inputs.legacy.importUtility "sops")
    ];
  };
  replace =
    {
      __argCodeEtlUpload__ = "${uploadGroup}/bin/${uploadGroup.name}";
    };
  name = "observes-scheduled-on-aws-code-etl-upload";
  entrypoint = projectPath "/makes/foss/units/observes/scheduled/on-aws/code-etl-upload/entrypoint.sh";
}
