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

  requirementsStr = builtins.concatStringsSep "\n" requirements;
  requirementsFile = builtins.toFile "requirements" requirementsStr;
in
  makeDerivation {
    builder = ./builder.sh;
    buildInputs = dependencies ++ [ python ];
    envRequirementsFile = requirementsFile;
    name = "build-python-requirements";
  }
