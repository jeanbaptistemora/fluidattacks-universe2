{
  fromYaml,
  inputs,
  makeDerivation,
  projectPath,
  ...
}: let
  lib = inputs.nixpkgs.lib;

  # Load data
  requirements = fromYaml (
    builtins.readFile (
      projectPath "/common/criteria/src/requirements/data.yaml"
    )
  );
  vulnerabilities = fromYaml (
    builtins.readFile (
      projectPath "/common/criteria/src/vulnerabilities/data.yaml"
    )
  );

  # Check if a requirement is supported by machine
  isReqSupportedInMachine = requirement: requirements.${requirement}.supported_in.machine;

  # Get list of requirements supported in machine
  supportedReqs = builtins.filter isReqSupportedInMachine (builtins.attrNames requirements);

  # Check if a vulnerability has at least one requirement supported in machine
  isVulnSupportedInMachine = vulnerability: let
    reqVuln = vulnerabilities.${vulnerability}.requirements;
    reqVulnInMachine = lib.lists.intersectLists reqVuln supportedReqs;
  in
    if (builtins.length reqVulnInMachine > 0)
    then true
    else false;

  # Get filtered list of vulnerabilities with any of its requirements supported in Machine
  supportedVulns = builtins.filter isVulnSupportedInMachine (builtins.attrNames vulnerabilities);

  # True if examples for the vulnerability are not empty, abort otherwise
  hasEmptyExamples = vulnerability: let
    exampleCompliant = vulnerabilities.${vulnerability}.examples.non_compliant;
    exampleNonCompliant = vulnerabilities.${vulnerability}.examples.non_compliant;
  in
    if ((exampleCompliant == "__empty__") || (exampleNonCompliant == "__empty__"))
    then abort "[ERROR] Vulnerability '${vulnerability}' has requirements supported by Machine but does not have code examples"
    else true;
in
  makeDerivation {
    env = {
      envExamples = builtins.map hasEmptyExamples supportedVulns;
    };
    builder = ''
      echo "[INFO] All machine supported vulnerabilities have code examples"
      touch $out
    '';
    name = "common-criteria-test-machine-examples";
  }
