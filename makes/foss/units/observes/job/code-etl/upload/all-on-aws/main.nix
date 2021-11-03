{ inputs
, outputs
, makeScript
, ...
}:
let
  uploadGroup = outputs."/computeOnAwsBatch/observesCodeEtlUpload";
in
makeScript {
  searchPaths = {
    source = [
      (outputs."/utils/aws")
      (inputs.legacy.importUtility "git")
      (inputs.legacy.importUtility "sops")
    ];
  };
  replace =
    {
      __argCodeEtlUpload__ = "${uploadGroup}/bin/${uploadGroup.name}";
    };
  name = "observes-job-code-etl-upload-all-on-aws";
  entrypoint = ./entrypoint.sh;
}
