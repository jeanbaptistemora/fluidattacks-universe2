# Do a npm install of the provided requirements
# Ensure they are fully pinned, even sub-dependencies

path: pkgs:

{ dependencies
, name
, node
, requirements
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path pkgs;
  nix = import (path "/makes/utils/nix") path pkgs;

  # Unpack arguments and sort them
  requirementsDirectSorted = nix.sortCaseless requirements.direct;
  requirementsInheritedSorted = nix.sortCaseless requirements.inherited;

  # Ensure the developer wrote them sorted
  # This helps with code clarity and maintainability
  requirementsDirect =
    if (requirementsDirectSorted == requirements.direct)
    then requirementsDirectSorted
    else abort "Direct requirements must be sorted in this order: ${builtins.toJSON requirementsDirectSorted}";
  requirementsInherited =
    if (requirementsInheritedSorted == requirements.inherited)
    then requirementsInheritedSorted
    else abort "Inherited requirements must be sorted in this order: ${builtins.toJSON requirementsInheritedSorted}";
  requirementsList = nix.sortCaseless (
    requirementsDirect ++
    requirementsInherited
  );

  # When dealing with a large number of packages, installing them all inline
  # throws a Bad Request error, so fall back to using a package.json file
  parsedRequirementsList = builtins.map (builtins.match "(.+)@(.+)") requirementsList;
  parsedRequirementsSet = builtins.listToAttrs (builtins.map (x: { name = builtins.head x; value = builtins.toString (builtins.tail x); }) parsedRequirementsList);
  packageJson = builtins.toJSON { "dependencies" = parsedRequirementsSet; };
in
makeDerivation {
  builder = path "/makes/utils/build-node-requirements/builder.sh";
  buildInputs = dependencies ++ [ pkgs.jq node ];
  envBashLibCommon = path "/makes/utils/common/template.sh";
  envPackageJsonFile = builtins.toFile "package.json" packageJson;
  envRequirementsFile = nix.listToFileWithTrailinNewLine requirementsList;
  name = "build-node-requirements-${name}";
}
