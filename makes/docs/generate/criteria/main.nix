{ asBashMap
, fromYaml
, inputs
, makeScript
, makeTemplate
, projectPath
, ...
}:
let
  # Extract model data
  data_vulnerabilities = fromYaml (
    builtins.readFile (
      projectPath "/makes/makes/criteria/src/vulnerabilities/data.yaml"));
  data_requirements = fromYaml (
    builtins.readFile (
      projectPath "/makes/makes/criteria/src/requirements/data.yaml"));
  data_compliance = fromYaml (
    builtins.readFile (
      projectPath "/makes/makes/criteria/src/compliance/data.yaml"));

  # Generate requirements list for a vulnerability
  vulnReq = id:
    "- [${id}. ${data_requirements.${id}.en.title}](/criteria2/requirements/${id})";
  reqsForVuln = reqs:
    builtins.concatStringsSep "\n" (builtins.map vulnReq reqs);

  # Generate definitions list for a requirement
  reqRefParseData = raw:
    let
      parsed = inputs.nixpkgs.lib.strings.splitString "." raw;
    in
    {
      standard = (builtins.head parsed);
      definition = (builtins.head (builtins.tail parsed));
    };
  reqRef = data:
    let
      standard = data_compliance.${data.standard};
      definition = standard.definitions.${data.definition};
    in
    "- [${standard.title}-${data.definition}: ${definition.title}](${definition.link})";
  refsForReq = refs:
    builtins.concatStringsSep "\n" (
      builtins.map reqRef (builtins.map reqRefParseData refs)
    );

  # Generate a template for every md
  makeVulnerability = name: src: makeTemplate {
    replace = {
      __argTitle__ = src.en.title;
      __argDescription__ = src.en.description;
      __argImpact__ = src.en.impact;
      __argRecommendation__ = src.en.recommendation;
      __argRequirements__ = reqsForVuln src.requirements;
    };
    name = "docs-make-vulnerability-${name}";
    template = ./templates/vulnerability.md;
  };
  makeRequirement = name: src: makeTemplate {
    replace = {
      __argTitle__ = src.en.title;
      __argSummary__ = src.en.summary;
      __argDescription__ = src.en.description;
      __argReferences__ = refsForReq src.references;
    };
    name = "docs-make-requirement-${name}";
    template = ./templates/requirement.md;
  };
  makeCompliance = name: src: makeTemplate {
    replace = {
      __argTitle__ = src.title;
      __argDescription__ = src.en.description;
    };
    name = "docs-make-compliance-${name}";
    template = ./templates/compliance.md;
  };
in
makeScript {
  name = "generate-criteria";
  replace = {
    __argVulnerabilities__ = asBashMap (
      builtins.mapAttrs makeVulnerability data_vulnerabilities
    );
    __argRequirements__ = asBashMap (
      builtins.mapAttrs makeRequirement data_requirements
    );
    __argCompliance__ = asBashMap (
      builtins.mapAttrs makeCompliance data_compliance
    );
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
    ];
  };
  entrypoint = ./entrypoint.sh;
}
