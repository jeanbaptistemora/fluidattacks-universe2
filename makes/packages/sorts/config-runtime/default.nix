{ fetchurl
, makeTemplate
, makes
, nixpkgs
, path
, ...
}:
let
  pythonRequirements = makes.makePythonPypiEnvironment {
    name = "sorts-runtime";
    searchPaths.bin = [ nixpkgs.gcc nixpkgs.postgresql ];
    sourcesYaml = ./pypi-sources.yaml;
  };
in
makeTemplate {
  arguments = {
    envSrcSortsSorts = path "/sorts/sorts";
  };
  name = "sorts-config-runtime";
  searchPaths = {
    envLibraries = [ nixpkgs.gcc.cc.lib ];
    envPaths = [
      nixpkgs.git
      nixpkgs.python38
    ];
    envPythonPaths = [
      (path "/sorts/sorts")
      (path "/sorts")
    ];
    envSources = [
      (makeTemplate {
        arguments = {
          envSortsModel = fetchurl {
            sha256 = "6QCH+jt8k8eGtu9ahSrsiypEwOAW86o42WvP+OSIbYE=";
            url = "https://sorts.s3.amazonaws.com/training-output/model.joblib?versionId=clsGZtxBJtqYdGgJsK9JOnaHpiBaD6to";
          };
          envSrcSortsStatic = path "/sorts/static";
        };
        name = "sorts-config-context-file";
        template = ''
          export SORTS_STATIC_PATH='__envSrcSortsStatic__'
          export SORTS_MODEL_PATH='__envSortsModel__'
        '';
      })
      pythonRequirements
    ];
  };
  template = path "/makes/packages/sorts/config-runtime/template.sh";
}
