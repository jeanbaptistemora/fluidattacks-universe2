# Do a pip install of the provided requirements
# Ensure they are fully pinned, even sub-dependencies

pkgs:

{
  dependencies,
  python,
  requirements,
}:

let
  makeDerivation = import ../../../makes/utils/make-derivation pkgs;

  sort = with pkgs.lib.strings; builtins.sort (a: b: toLower a < toLower b);

  # Unpack arguments and sort them
  requirementsDirectSorted = sort requirements.direct;
  requirementsInheritedSorted = sort requirements.inherited;

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
  requirementsList = sort (
    requirementsDirect ++
    requirementsInherited
  );

  requirementsStr = builtins.concatStringsSep "\n" requirementsList;
  requirementsFile = builtins.toFile "requirements" requirementsStr;
in
  makeDerivation {
    builder = ./builder.sh;
    buildInputs = dependencies ++ [ python ];
    envRequirementsFile = requirementsFile;
    name = "build-python-requirements";
  }
