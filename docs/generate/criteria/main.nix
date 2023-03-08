{
  toBashMap,
  calculateCvss3,
  fromJson,
  fromYaml,
  inputs,
  makeScript,
  makeTemplate,
  stringCapitalize,
  ...
}: let
  lib = inputs.nixpkgs.lib;

  # Model data
  compliance = fromYaml (
    builtins.readFile (
      inputs.nixpkgs.fetchurl {
        url = "https://gitlab.com/fluidattacks/universe/-/raw/9e14b8fcb497863279af8887d263de5d6b609c87/common/criteria/src/compliance/data.yaml";
        sha256 = "sha256-yyoXUBU/HgsDVoUp2kmKLPyRKgPdmnY1OB4S+OvFk1I=";
      }
    )
  );
  requirements = fromYaml (
    builtins.readFile (
      inputs.nixpkgs.fetchurl {
        url = "https://gitlab.com/fluidattacks/universe/-/raw/9e14b8fcb497863279af8887d263de5d6b609c87/common/criteria/src/requirements/data.yaml";
        sha256 = "sha256-rPlbIzSFxmzlob/2zt1bLSI8iP75UJofJ1mpVDt3ChE=";
      }
    )
  );
  vulnerabilities = fromYaml (
    builtins.readFile (
      inputs.nixpkgs.fetchurl {
        url = "https://gitlab.com/fluidattacks/universe/-/raw/9e14b8fcb497863279af8887d263de5d6b609c87/common/criteria/src/vulnerabilities/data.yaml";
        sha256 = "sha256-5FJH31x2s/rsOkamYaCRXF6JDPIexU6co1CbN7R9F2U=";
      }
    )
  );

  # Title and content
  section = {
    title,
    content,
  }:
    if content != "__empty__" && content != ""
    then "${title}\n\n${content}"
    else "";

  # Category path for a vulnerability or requirement
  categoryPath = id: data: let
    category = stringCapitalize data.category;
  in "${category}/${id}";

  # Parse a reference to a definition
  parseDefinition = reference: let
    parsed = lib.strings.splitString "." reference;
  in {
    standardId = builtins.head parsed;
    definitionId = builtins.head (builtins.tail parsed);
  };

  # True if a vulnerability has a requirement, false otherwise
  hasRequirement = {
    requirementId,
    vulnerabilityId,
  }:
    builtins.any
    (x: x == requirementId)
    vulnerabilities.${vulnerabilityId}.requirements;

  # True if a requirement has a definition, false otherwise
  hasDefinition = {
    requirementId,
    standardId,
    definitionId,
  }:
    builtins.any
    (x: x == "${standardId}.${definitionId}")
    requirements.${requirementId}.references;

  # Markdown links
  link = {
    prefix ? "",
    body,
    path,
  }: "${prefix}[${body}](${path})";
  linkRequirement = {
    prefix ? "- ",
    id,
  }:
    link {
      inherit prefix;
      body = "${id}. ${requirements.${id}.en.title}";
      path = "/criteria/requirements/${id}";
    };
  linkVulnerability = {
    prefix ? "- ",
    id,
  }:
    link {
      inherit prefix;
      body = "${id}. ${vulnerabilities.${id}.en.title}";
      path = "/criteria/vulnerabilities/${id}";
    };
  linkStandardDefinition = {
    prefix ? "- ",
    standardId,
    definitionId,
  }: let
    standard = compliance.${standardId};
    definition = standard.definitions.${definitionId};
  in
    link {
      inherit prefix;
      body = "${standard.title}-${definitionId}. ${definition.title}";
      path = "/criteria/compliance/${standardId}";
    };
  linkDefinition = {
    prefix ? "",
    standardId,
    definitionId,
  }: let
    standard = compliance.${standardId};
    definition = standard.definitions.${definitionId};
  in
    link {
      inherit prefix;
      body = "${definitionId}. ${definition.title}";
      path = definition.link;
    };
  linkStandard = {
    prefix ? "- ",
    standardId,
  }: let
    standard = compliance.${standardId};
  in
    link {
      inherit prefix;
      body = " ${standard.title}";
      path = "/criteria/compliance/${standardId}";
    };

  # Markdown image
  image = {
    title,
    path,
  }: "![${title}](${path})";

  # Score and severity for a vulnerability
  vectorString = vector: let
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
  cvssScore = vector:
    fromJson (builtins.readFile (calculateCvss3 (vectorString vector)));

  # Requirements list for a vulnerability
  vulnerabilityRequirements = vulnerabilityId: let
    requirements = vulnerabilities.${vulnerabilityId}.requirements;
  in
    builtins.concatStringsSep "\n" (
      builtins.map
      (id:
        linkRequirement {
          inherit id;
        })
      requirements
    );

  # Remediation times for a vulnerability
  vulnerabilitiesRemediationTime = vulnerabilityId: let
    remediationTime = vulnerabilities.${vulnerabilityId}.remediation_time;
  in "⌚ ${remediationTime} minutes.";

  # Compliant and non-compliant code
  codeExamples = examples: let
    compliant = section {
      title = "### Compliant code";
      content = examples.compliant;
    };
    non_compliant = section {
      title = "### Non compliant code";
      content = examples.non_compliant;
    };
  in
    section {
      title = "## Code Examples";
      content = compliant + non_compliant;
    };

  # Requirements list for a definition
  definitionRequirements = {
    standardId,
    definitionId,
  }: let
    filtered = builtins.attrNames (
      lib.filterAttrs
      (requirementId: _:
        hasDefinition {
          inherit requirementId;
          inherit standardId;
          inherit definitionId;
        })
      requirements
    );
  in
    builtins.concatStringsSep "<br />" (
      builtins.map
      (id:
        linkRequirement {
          prefix = "";
          inherit id;
        })
      filtered
    );

  # Table for plans that support requirement
  requirementsSupportedIn = requirementId: let
    supportedIn = requirements.${requirementId}.supported_in;
    isSupported = subs:
      if subs
      then "🟢"
      else "🔴";
    machineLink = link {
      body = "Machine";
      path = "https://fluidattacks.com/services/continuous-hacking/";
    };
    squadLink = link {
      body = "Squad";
      path = "https://fluidattacks.com/services/continuous-hacking/";
    };
    oneshotLink = link {
      body = "One-Shot";
      path = "https://fluidattacks.com/services/one-shot-hacking/";
    };
    showTable = builtins.any (x: x) (builtins.attrValues supportedIn);
  in
    if showTable
    then ''
      This requirement is verified in following services:

        | Plan     | Supported              |
        | :------: | :--------------------: |
        | ${machineLink} | ${isSupported supportedIn.machine} |
        | ${squadLink}   | ${isSupported supportedIn.squad}   |
        | ${oneshotLink} | ${isSupported supportedIn.oneshot} |
    ''
    else "";

  # References list for a requirement
  requirementReferences = requirementId: let
    references = requirements.${requirementId}.references;
    parsed = builtins.map parseDefinition references;
  in
    builtins.concatStringsSep "\n" (
      builtins.map
      (reference:
        with reference;
          linkStandardDefinition {
            inherit definitionId;
            inherit standardId;
          })
      parsed
    );

  # Vulnerabilities list for a requirement
  requirementVulnerabilities = requirementId: let
    filtered = builtins.attrNames (
      lib.filterAttrs
      (vulnerabilityId: _:
        hasRequirement {
          inherit requirementId;
          inherit vulnerabilityId;
        })
      vulnerabilities
    );
  in
    builtins.concatStringsSep "\n" (
      builtins.map
      (id:
        linkVulnerability {
          inherit id;
        })
      filtered
    );

  # Definition with requirements
  definitionWithRequirements = {
    standardId,
    definitionId,
  }: let
    definition = linkDefinition {
      inherit standardId;
      inherit definitionId;
    };
    requirements = definitionRequirements {
      inherit standardId;
      inherit definitionId;
    };
    result =
      if requirements != ""
      then "| ${definition} | ${requirements} |"
      else "| ${definition} | - |";
  in
    result;

  # Standard definitions with requirements
  standardDefinitionsWithRequirements = standardId: let
    definitions = lib.lists.naturalSort (builtins.attrNames compliance.${standardId}.definitions);
  in
    ''
      | Definition | Requirements |
      | : -------  | :----------- |
    ''
    + builtins.concatStringsSep "\n" (
      builtins.map
      (definitionId:
        definitionWithRequirements {
          inherit standardId;
          inherit definitionId;
        })
      definitions
    );

  # Introduction indexes
  categoryLinks = {
    type,
    category,
    data,
  }: let
    filtered = lib.attrsets.filterAttrs (_: v: v.category == category) data;
  in
    "### ${category}\n"
    + builtins.concatStringsSep "\n" (builtins.attrValues (
      builtins.mapAttrs
      (k: v: "- [${k}. ${v.en.title}](/criteria/${type}/${k})")
      filtered
    ));
  index = {
    type,
    data,
  }: let
    categories = builtins.sort builtins.lessThan (
      lib.lists.unique (
        builtins.map (x: x.category) (builtins.attrValues data)
      )
    );
  in
    builtins.concatStringsSep "\n" (
      builtins.map
      (category:
        categoryLinks {
          inherit type;
          inherit category;
          inherit data;
        })
      categories
    );

  # Introduction index for Compliance
  indexCompliance = {data}:
    builtins.concatStringsSep "\n"
    (
      builtins.map
      (
        standardId:
          linkStandard
          {
            inherit standardId;
          }
      )
      (
        builtins.attrNames
        data
      )
    );

  # Generate a template for every introduction
  makeIntroVulnerabilities = makeTemplate {
    replace = {
      __argIndex__ = index {
        type = "vulnerabilities";
        data = vulnerabilities;
      };
    };
    name = "docs-make-intro-vulnerabilities";
    template = ./templates/intros/vulnerability.md;
    local = false;
  };
  makeIntroRequirements = makeTemplate {
    replace = {
      __argIndex__ = index {
        type = "requirements";
        data = requirements;
      };
    };
    name = "docs-make-intro-requirements";
    template = ./templates/intros/requirement.md;
    local = false;
  };
  makeIntroCompliance = makeTemplate {
    replace = {
      __argIndex__ = indexCompliance {
        data = compliance;
      };
    };
    name = "docs-make-intro-compliance";
    template = ./templates/intros/compliance.md;
    local = false;
  };

  # Generate a template for every md
  makeVulnerability = __argCode__: src: let
    score = cvssScore src.score;
  in
    makeTemplate {
      replace = {
        inherit __argCode__;
        __argTitle__ = src.en.title;
        __argDescription__ = section {
          title = "## Description";
          content = src.en.description;
        };
        __argImpact__ = section {
          title = "## Impact";
          content = src.en.impact;
        };
        __argRecommendation__ = section {
          title = "## Recommendation";
          content = src.en.recommendation;
        };
        __argThreat__ = section {
          title = "## Threat";
          content = src.en.threat;
        };
        __argRemediationTime__ = section {
          title = "## Expected Remediation Time";
          content = vulnerabilitiesRemediationTime __argCode__;
        };
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
        __argExamples__ = codeExamples src.examples;
        __argDetails__ = section {
          title = "## Details";
          content = src.metadata.en.details;
        };
        __argRequirements__ = section {
          title = "## Requirements";
          content = vulnerabilityRequirements __argCode__;
        };
      };
      name = "docs-make-vulnerability-${__argCode__}";
      template = ./templates/vulnerability.md;
      local = false;
    };
  makeRequirement = __argCode__: src:
    makeTemplate {
      replace = {
        inherit __argCode__;
        __argTitle__ = src.en.title;
        __argSummary__ = section {
          title = "## Summary";
          content = src.en.summary;
        };
        __argDescription__ = section {
          title = "## Description";
          content = src.en.description;
        };
        __argSupportedIn__ = section {
          title = "## Supported In";
          content = requirementsSupportedIn __argCode__;
        };
        __argReferences__ = section {
          title = "## References";
          content = requirementReferences __argCode__;
        };
        __argVulnerabilities__ = section {
          title = "## Vulnerabilities";
          content = requirementVulnerabilities __argCode__;
        };
      };
      name = "docs-make-requirement-${__argCode__}";
      template = ./templates/requirement.md;
      local = false;
    };
  makeCompliance = __argCode__: src:
    makeTemplate {
      replace = {
        inherit __argCode__;
        __argLogo__ = image {
          title = "logo";
          path = builtins.concatStringsSep "" [
            "https://res.cloudinary.com"
            "/fluid-attacks/image/upload"
            "/c_scale,w_256"
            "/docs/criteria/compliance/logos/${__argCode__}.png"
          ];
        };
        __argTitle__ = src.title;
        __argSummary__ = section {
          title = "## Summary";
          content = src.en.summary;
        };
        __argDefinitions__ = section {
          title = "## Definitions";
          content = standardDefinitionsWithRequirements __argCode__;
        };
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
        (k: v: lib.nameValuePair (categoryPath k v) (makeVulnerability k v))
        vulnerabilities
      );
      __argRequirements__ = toBashMap (
        lib.mapAttrs'
        (k: v: lib.nameValuePair (categoryPath k v) (makeRequirement k v))
        requirements
      );
      __argCompliance__ = toBashMap (
        builtins.mapAttrs makeCompliance compliance
      );
    };
    searchPaths.bin = [inputs.nixpkgs.git];
    entrypoint = ./entrypoint.sh;
  }
