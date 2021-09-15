{ fromYaml
, inputs
, makeDerivation
, projectPath
, ...
}:
let
  lib = inputs.nixpkgs.lib;

  # Load data
  compliance = fromYaml (
    builtins.readFile (
      projectPath "/makes/foss/modules/makes/criteria/src/compliance/data.yaml"));
  requirements = fromYaml (
    builtins.readFile (
      projectPath "/makes/foss/modules/makes/criteria/src/requirements/data.yaml"));
  vulnerabilities = fromYaml (
    builtins.readFile (
      projectPath "/makes/foss/modules/makes/criteria/src/vulnerabilities/data.yaml"));

  # Get list of references
  references = field: data: lib.lists.unique (
    lib.lists.flatten (
      builtins.map (x: x.${field}) (builtins.attrValues data)
    )
  );

  # List of referenced requirements in vulnerabilities
  referencedReqs = references "requirements" vulnerabilities;

  # List of referenced complaince definitions in requirements
  referencedDefs = references "references" requirements;

  # True if requirement exists, abort otherwise
  hasRequirement = requirement:
    if (builtins.hasAttr requirement requirements)
    then true
    else abort "[ERROR] Requirement '${requirement}' was referenced but does not exist.";

  # True if definition exists, abort otherwise
  hasDefinition = path:
    let
      parsedPath = lib.strings.splitString "." path;
      standard = builtins.elemAt parsedPath 0;
      definition = builtins.elemAt parsedPath 1;
    in
    if (lib.attrsets.hasAttrByPath [ standard "definitions" definition ] compliance)
    then true
    else abort "[ERROR] Standard '${standard}' with definition '${definition}' was referenced but does not exist.";
in
makeDerivation {
  env = {
    envRequirements = builtins.map hasRequirement referencedReqs;
    envDefinitions = builtins.map hasDefinition referencedDefs;
  };
  builder = ''
    echo "[INFO] Test passed."
    touch $out
  '';
  name = "criteria-test";
}
