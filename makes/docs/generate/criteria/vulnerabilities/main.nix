{ fromYaml
, makeTemplate
, makeDerivationParallel
, projectPath
, ...
}:
let
  vulnerabilities = fromYaml (
    builtins.readFile (
      projectPath "/makes/makes/criteria/src/vulnerabilities/data.yaml"));

  generateVulnerability = name: src: makeTemplate {
    replace = {
      __argDescription__ = src.en.description;
      __argImpact__ = src.en.impact;
      __argRecommendation__ = src.en.recommendation;
    };
    name = "docs-generate-vulnerability-${name}";
    template = ./template.md;
  };
in
makeDerivationParallel {
  dependencies = builtins.mapAttrs generateVulnerability vulnerabilities;
  name = "generate-vulnerabilities";
}
