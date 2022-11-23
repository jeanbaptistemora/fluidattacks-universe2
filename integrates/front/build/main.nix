{
  inputs,
  makeDerivation,
  outputs,
  projectPath,
  ...
}:
makeDerivation {
  env = {
    envExternalC3 = inputs.nixpkgs.fetchzip {
      url = "https://github.com/c3js/c3/archive/v0.7.20.zip";
      sha256 = "tnKDZjobbxLkat2WZ+CN+AU526JUOk51vq86miGRVPI=";
    };
    envSetupIntegratesFrontDevRuntime =
      outputs."/integrates/front/config/dev-runtime";
    envIntegratesBackAppTemplates = projectPath "/integrates/back/src/app/templates/static";
    envIntegratesFront = projectPath "/integrates/front";
  };
  builder = ./builder.sh;
  name = "integrates-front-build";
  searchPaths = {
    bin = [
      inputs.nixpkgs.bash
      inputs.nixpkgs.patch
    ];
    source = [outputs."/integrates/front/config/dev-runtime-env"];
  };
}
