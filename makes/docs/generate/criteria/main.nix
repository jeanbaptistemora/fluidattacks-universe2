{ toBashMap
, calculateCvss3
, fromJson
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

  # Generate score and severity for a vulnerability
  vectorString = vector:
    let
      AV = vector.base.attack_vector;
      AC = vector.base.attack_complexity;
      PR = vector.base.privileges_required;
      UI = vector.base.user_interaction;
      S = vector.base.scope;
      C = vector.base.confidentiality;
      I = vector.base.integrity;
      A = vector.base.availability;
      E = vector.temporal.exploit_code_maturity;
      RL = vector.temporal.remediation_level;
      RC = vector.temporal.report_confidence;
    in
    "CVSS:3.1/AV:${AV}/AC:${AC}/PR:${PR}/UI:${UI}/S:${S}/C:${C}/I:${I}/A:${A}/E:${E}/RL:${RL}/RC:${RC}";
  vulnScore = vector:
    fromJson (builtins.readFile (calculateCvss3 (vectorString vector)));

  # Generate requirements list for a vulnerability
  vulnReq = id:
    "- [${id}. ${data_requirements.${id}.en.title}](/criteria2/requirements/${id})";
  reqsForVuln = reqs:
    builtins.concatStringsSep "\n" (builtins.map vulnReq reqs);

  # Generate references list for a requirement
  reqRefParseData = raw:
    let
      parsed = inputs.nixpkgs.lib.strings.splitString "." raw;
    in
    {
      standard_id = (builtins.head parsed);
      definition_id = (builtins.head (builtins.tail parsed));
    };
  reqRef = data:
    let
      standard = data_compliance.${data.standard_id};
      standard_link = "/criteria2/compliance/${data.standard_id}";
      definition = standard.definitions.${data.definition_id};
    in
    "- [${standard.title}-${data.definition_id}: ${definition.title}](${standard_link})";
  refsForReq = refs:
    builtins.concatStringsSep "\n" (
      builtins.map reqRef (
        builtins.map reqRefParseData refs
      )
    );

  # Generate definitions list for a standard
  standardDef = id: def:
    "- [${id}. ${def.title}](${def.link})";
  defsForStandard = defs:
    builtins.concatStringsSep "\n" (
      builtins.attrValues (
        builtins.mapAttrs standardDef defs
      )
    );

  # Generate a template for every md
  makeVulnerability = name: src: makeTemplate {
    replace = {
      __argTitle__ = src.en.title;
      __argDescription__ = src.en.description;
      __argImpact__ = src.en.impact;
      __argRecommendation__ = src.en.recommendation;
      __argThreat__ = src.en.threat;
      __argScoreBaseAttackVector__ = src.score.base.attack_vector;
      __argScoreBaseAttackComplexity__ = src.score.base.attack_complexity;
      __argScoreBasePrivilegesRequired__ = src.score.base.privileges_required;
      __argScoreBaseUserInteraction__ = src.score.base.user_interaction;
      __argScoreBaseScope__ = src.score.base.scope;
      __argScoreBaseConfidentiality__ = src.score.base.confidentiality;
      __argScoreBaseIntegrity__ = src.score.base.integrity;
      __argScoreBaseAvailability__ = src.score.base.availability;
      __argScoreTemporalExploitCodeMadurity__ = src.score.temporal.exploit_code_maturity;
      __argScoreTemporalRemediationLevel__ = src.score.temporal.remediation_level;
      __argScoreTemporalReportConfidence__ = src.score.temporal.report_confidence;
      __argVectorString__ = vectorString src.score;
      __argScoreBase__ = (vulnScore src.score).score.base;
      __argScoreTemporal__ = (vulnScore src.score).score.temporal;
      __argSeverityBase__ = (vulnScore src.score).severity.base;
      __argSeverityTemporal__ = (vulnScore src.score).severity.temporal;
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
      __argDefinitions__ = defsForStandard src.definitions;
    };
    name = "docs-make-compliance-${name}";
    template = ./templates/compliance.md;
  };
in
makeScript {
  name = "generate-criteria";
  replace = {
    __argVulnerabilities__ = toBashMap (
      builtins.mapAttrs makeVulnerability data_vulnerabilities
    );
    __argRequirements__ = toBashMap (
      builtins.mapAttrs makeRequirement data_requirements
    );
    __argCompliance__ = toBashMap (
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
