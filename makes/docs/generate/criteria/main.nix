{ toBashMap
, calculateCvss3
, fromJson
, fromYaml
, inputs
, makeScript
, makeTemplate
, projectPath
, stringCapitalize
, ...
}:
let
  lib = inputs.nixpkgs.lib;

  # Title and content
  section = title: content:
    if content != "__empty__" && content != ""
    then "${title}\n\n${content}"
    else "";

  # Category path for a vulnerability or requirement
  categoryPath = id: data:
    let
      category = stringCapitalize data.category;
    in
    "${category}/${id}";

  # Extract model data
  vulnerabilities = fromYaml (
    builtins.readFile (
      projectPath "/makes/makes/criteria/src/vulnerabilities/data.yaml"));
  requirements = fromYaml (
    builtins.readFile (
      projectPath "/makes/makes/criteria/src/requirements/data.yaml"));
  compliance = fromYaml (
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
    builtins.concatStringsSep "" [
      "CVSS:3.1"
      "/AV:${AV}/AC:${AC}/PR:${PR}/UI:${UI}/S:${S}/C:${C}/I:${I}/A:${A}"
      "/E:${E}/RL:${RL}/RC:${RC}"
    ];
  vulnScore = vector:
    fromJson (builtins.readFile (calculateCvss3 (vectorString vector)));

  # Generate requirements list for a vulnerability
  vulnReq = id:
    "- [${id}. ${requirements.${id}.en.title}](/criteria/requirements/${id})";
  reqsForVuln = reqs:
    builtins.concatStringsSep "\n" (builtins.map vulnReq reqs);

  # Generate references list for a requirement
  reqRefParseData = raw:
    let
      parsed = lib.strings.splitString "." raw;
    in
    {
      standardId = (builtins.head parsed);
      definitionId = (builtins.head (builtins.tail parsed));
    };
  reqRef = data:
    let
      standard = compliance.${data.standardId};
      standardLink = "/criteria/compliance/${data.standardId}";
      definition = standard.definitions.${data.definitionId};
    in
    builtins.concatStringsSep "" [
      "- [${standard.title}-${data.definitionId}: ${definition.title}]"
      "(${standardLink})"
    ];
  refsForReq = refs:
    builtins.concatStringsSep "\n" (
      builtins.map reqRef (
        builtins.map reqRefParseData refs
      )
    );

  # Generate vulnerabilities list for a requirement
  vulnHasReq = req: vuln:
    builtins.any (x: x == req) vulnerabilities.${vuln}.requirements;
  reqVuln = id:
    let
      title = vulnerabilities.${id}.en.title;
    in
    "- [${id}. ${title}](/criteria/vulnerabilities/${id})";
  vulnsForReq = req:
    let
      vulns = builtins.attrNames (
        lib.filterAttrs (id: _: vulnHasReq req id) vulnerabilities
      );
    in
    builtins.concatStringsSep "\n" (
      builtins.map reqVuln vulns
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

  # Generate introduction indexes
  categories = data: builtins.sort builtins.lessThan (lib.lists.unique (
    builtins.map (x: x.category) (builtins.attrValues data)));
  itemsByCategory = category: lib.attrsets.filterAttrs
    (_: v: v.category == category);
  linksByCategory = type: category: data:
    "### ${category}\n" + builtins.concatStringsSep "\n" (
      builtins.attrValues (builtins.mapAttrs
        (k: v: "- [${k}. ${v.en.title}](/criteria/${type}/${k})")
        (itemsByCategory category data)
      )
    );
  links = type: data: builtins.concatStringsSep "\n" (
    builtins.map
      (category: linksByCategory type category data)
      (categories data)
  );

  # Generate a template for every introduction
  makeIntroVulnerabilities = makeTemplate {
    replace = {
      __argIndex__ = links "vulnerabilities" vulnerabilities;
    };
    name = "docs-make-intro-vulnerabilities";
    template = ./templates/intros/vulnerability.md;
    local = false;
  };
  makeIntroRequirements = makeTemplate {
    replace = {
      __argIndex__ = links "requirements" requirements;
    };
    name = "docs-make-intro-requirements";
    template = ./templates/intros/requirement.md;
    local = false;
  };
  makeIntroCompliance = makeTemplate {
    name = "docs-make-intro-compliance";
    template = ./templates/intros/compliance.md;
    local = false;
  };

  # Generate a template for every md
  makeVulnerability = __argCode__: src:
    let
      score = vulnScore src.score;
    in
    makeTemplate {
      replace = {
        inherit __argCode__;
        __argTitle__ = src.en.title;
        __argDescription__ = section "## Description" src.en.description;
        __argImpact__ = section "## Impact" src.en.impact;
        __argRecommendation__ =
          section "## Recommendation" src.en.recommendation;
        __argThreat__ = section "## Threat" src.en.threat;
        __argScoreBaseAttackVector__ = src.score.base.attack_vector;
        __argScoreBaseAttackComplexity__ = src.score.base.attack_complexity;
        __argScoreBasePrivilegesRequired__ = src.score.base.privileges_required;
        __argScoreBaseUserInteraction__ = src.score.base.user_interaction;
        __argScoreBaseScope__ = src.score.base.scope;
        __argScoreBaseConfidentiality__ = src.score.base.confidentiality;
        __argScoreBaseIntegrity__ = src.score.base.integrity;
        __argScoreBaseAvailability__ = src.score.base.availability;
        __argScoreTemporalExploitCodeMadurity__ =
          src.score.temporal.exploit_code_maturity;
        __argScoreTemporalRemediationLevel__ =
          src.score.temporal.remediation_level;
        __argScoreTemporalReportConfidence__ =
          src.score.temporal.report_confidence;
        __argVectorString__ = vectorString src.score;
        __argScoreBase__ = score.score.base;
        __argScoreTemporal__ = score.score.temporal;
        __argSeverityBase__ = score.severity.base;
        __argSeverityTemporal__ = score.severity.temporal;
        __argDetails__ = section "## Details" src.metadata.en.details;
        __argRequirements__ =
          section "## Requirements" (reqsForVuln src.requirements);
      };
      name = "docs-make-vulnerability-${__argCode__}";
      template = ./templates/vulnerability.md;
      local = false;
    };
  makeRequirement = __argCode__: src: makeTemplate {
    replace = {
      inherit __argCode__;
      __argTitle__ = src.en.title;
      __argSummary__ = section "## Summary" src.en.summary;
      __argDescription__ = section "## Description" src.en.description;
      __argReferences__ = section "## References" (refsForReq src.references);
      __argVulnerabilities__ =
        section "## Vulnerabilities" (vulnsForReq __argCode__);
    };
    name = "docs-make-requirement-${__argCode__}";
    template = ./templates/requirement.md;
    local = false;
  };
  makeCompliance = __argCode__: src: makeTemplate {
    replace = {
      inherit __argCode__;
      __argTitle__ = src.title;
      __argDescription__ = section "## Description" src.en.description;
      __argDefinitions__ =
        section "## Definitions" (defsForStandard src.definitions);
    };
    name = "docs-make-compliance-${__argCode__}";
    template = ./templates/compliance.md;
    local = false;
  };
in
makeScript {
  name = "generate-criteria";
  replace = {
    __argIntroVulnerabilities__ = makeIntroVulnerabilities;
    __argIntroRequirements__ = makeIntroRequirements;
    __argIntroCompliance__ = makeIntroCompliance;
    __argVulnerabilities__ = toBashMap (
      lib.mapAttrs'
        (
          k: v: lib.nameValuePair (categoryPath k v) (makeVulnerability k v)
        )
        vulnerabilities
    );
    __argRequirements__ = toBashMap (
      lib.mapAttrs'
        (
          k: v: lib.nameValuePair (categoryPath k v) (makeRequirement k v)
        )
        requirements
    );
    __argCompliance__ = toBashMap (
      builtins.mapAttrs makeCompliance compliance
    );
  };
  searchPaths.bin = [ inputs.nixpkgs.git ];
  entrypoint = ./entrypoint.sh;
}
