{ asBashMap
, fromYaml
, makeScript
, makeTemplate
, projectPath
, ...
}:
let
  data = fromYaml (
    builtins.readFile (
      projectPath "/makes/makes/criteria/src/vulnerabilities/data.yaml"));
  makeVuln = name: src: makeTemplate {
    replace = {
      __argTitle__ = src.en.title;
      __argDescription__ = src.en.description;
      __argImpact__ = src.en.impact;
      __argRecommendation__ = src.en.recommendation;
    };
    name = "docs-make-vuln-${name}";
    template = ./template.md;
  };
in
makeScript {
  name = "generate-criteria-vulns";
  replace = {
    __argVulns__ = asBashMap (builtins.mapAttrs makeVuln data);
  };
  entrypoint = ./entrypoint.sh;
}
