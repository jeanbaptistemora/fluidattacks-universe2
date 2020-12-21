# Do a pip install of the provided requirements
# Ensure they are fully pinned, even sub-dependencies

pkgs:

{
  dependencies,
  python,
  requirements,
}:

let
  make = import ../../../makes/utils/make pkgs;

  requirementsStr = builtins.concatStringsSep "\n" requirements;
  requirementsFile = builtins.toFile "requirements" requirementsStr;
in
  make {
    builder = ./builder.sh;
    buildInputs = dependencies ++ [ python ];
    envRequirementsFile = requirementsFile;
    name = "build-python-requirements";
  }
