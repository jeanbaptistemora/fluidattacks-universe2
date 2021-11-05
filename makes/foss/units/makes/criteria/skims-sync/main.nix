{ fromJson
, fromYaml
, makeDerivation
, projectPath
, ...
}:
let
  # Load Data
  criteria = fromYaml (
    builtins.readFile (
      projectPath "/makes/foss/modules/makes/criteria/src/vulnerabilities/data.yaml"));
  skimsManifest = fromJson (
    builtins.readFile (
      projectPath "/skims/manifests/findings.json"));

  criteriaFindings = builtins.map
    (
      x: builtins.concatStringsSep ". " [ x (builtins.getAttr x criteria).en.title ]
    )
    (builtins.attrNames criteria);
  skimsFindings = builtins.map (x: x.EN.title) (builtins.attrValues skimsManifest);
  unsyncedFindings = builtins.filter
    (
      finding: ! builtins.elem finding criteriaFindings
    )
    skimsFindings;

  areFindingsUnsynced = findings:
    if (builtins.length findings > 0)
    then abort "\n[ERROR] Findings:\n${builtins.concatStringsSep "\n" unsyncedFindings}\nin Skims are not in sync with the criteria"
    else true;
in
makeDerivation {
  env = {
    envUnsyncedFindings = areFindingsUnsynced unsyncedFindings;
  };
  builder = ''
    info "Criteria and Skims findings are in sync."
    touch $out
  '';
  name = "criteria-skims-sync";
}
