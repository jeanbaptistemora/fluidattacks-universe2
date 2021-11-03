{ inputs
, makeScript
, outputs
, projectPath
, ...
} @ _:
makeScript {
  replace = {
    __argSecretsProd__ = projectPath "/integrates/secrets-production.yaml";
  };
  name = "integrates-mobile-deploy-playstore";
  searchPaths = {
    bin = [
      inputs.nixpkgs.git
      inputs.nixpkgs.nodejs-12_x
      inputs.nixpkgs.ruby
    ];
    source = [
      outputs."/integrates/mobile/tools"
      (outputs."/utils/aws")
      (outputs."/utils/git")
      (outputs."/utils/sops")
    ];
  };
  entrypoint = projectPath "/makes/foss/units/integrates/mobile/deploy/playstore/entrypoint.sh";
}
