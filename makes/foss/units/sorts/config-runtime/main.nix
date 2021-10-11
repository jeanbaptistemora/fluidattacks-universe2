{ fetchUrl
, inputs
, makePythonPypiEnvironment
, makeTemplate
, projectPath
, ...
}:
let
  pythonRequirements = makePythonPypiEnvironment {
    name = "sorts-runtime";
    searchPaths.bin = [
      inputs.nixpkgs.gcc
      inputs.nixpkgs.postgresql
    ];
    sourcesYaml = ./pypi-sources.yaml;
  };
in
makeTemplate {
  replace = {
    __argSrcSortsSorts__ = projectPath "/sorts/sorts";
  };
  name = "sorts-config-runtime";
  searchPaths = {
    rpath = [
      inputs.nixpkgs.gcc.cc.lib
    ];
    bin = [
      inputs.nixpkgs.git
      inputs.nixpkgs.python38
    ];
    pythonPackage = [
      (projectPath "/sorts/sorts")
      (projectPath "/sorts")
    ];
    source = [
      (makeTemplate {
        replace = {
          __argSortsModel__ = fetchUrl {
            sha256 = "6QCH+jt8k8eGtu9ahSrsiypEwOAW86o42WvP+OSIbYE=";
            url = "https://sorts.s3.amazonaws.com/training-output/model.joblib?versionId=clsGZtxBJtqYdGgJsK9JOnaHpiBaD6to";
          };
          __argSrcSortsStatic__ = projectPath "/sorts/static";
        };
        name = "sorts-config-context-file";
        template = ''
          export SORTS_STATIC_PATH='__argSrcSortsStatic__'
          export SORTS_MODEL_PATH='__argSortsModel__'
        '';
      })
      pythonRequirements
    ];
  };
  template = projectPath "/makes/foss/units/sorts/config-runtime/template.sh";
}
