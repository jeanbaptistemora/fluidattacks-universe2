# Do a pip install of the provided requirements
# Ensure they are fully pinned, even sub-dependencies

path: pkgs:

{ dependencies
, python
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
in
makeDerivation {
  builder = path "/makes/utils/build-python-requirements/builder.sh";
  buildInputs = dependencies ++ [ python ];
  envRequirementsFile = nix.listToFileWithTrailinNewLine requirementsList;
  name = "build-python-requirements";
}
